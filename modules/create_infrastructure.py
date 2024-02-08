#!/usr/bin/env python3

from .create_params import (
    is_nfcore,
    question_config_owner,
    retrieve_computational_resources,
    question_max_resources,
)
from .create_hpc_env import (
    check_scheduler, 
    check_queues,
    check_modules,
)
from .write_config import write_config
from colorama import Fore, Style, init
import inquirer
from .create_container import create_container_scope

# Initialise colorama
init(autoreset=True)


def create_infrastructure():
    ## Basic information
    nfcore_config = is_nfcore()
    nfcore_params = None

    ## Config description and resources
    if nfcore_config["nfcore_question"]:
        nfcore_params = question_config_owner()

    ## Infrastructure type
    execution_env_question = [
        inquirer.List(
            "executor_env",
            message="What type of execution environment are you working in?",
            choices=["hpc", "local"],
        ),
    ]
    answers = inquirer.prompt(execution_env_question)
    executor_env = answers["executor_env"]

    scheduler_name = None  # Save name of scheduler if hpc selected
    queue_name = None # Save list of queues if job scheduler detected 
    module_results = None  # Save name of module if found

    # Printing the selected environment
    print(f"You selected: {executor_env}.\n")

    # Infra-type specific options (in future could add cloud e.g. for AWS specific scopes)
    if executor_env == "hpc":
        scheduler_name = check_scheduler()
        if scheduler_name != "none":
            print(f"The detected job scheduler is: {scheduler_name}.\n")
            queue_name = check_queues(scheduler_name)  # Pass the result of check_scheduler
        module_results = check_modules()

    else:
        pass

    print(Fore.YELLOW + "Checking for available software environment software...")
    container_results = create_container_scope()
    print(f"You selected: {container_results['container_options']}.\n")

    # Maximum resources (asked regardless if HPC or local)
    if nfcore_config["nfcore_question"]:
        if executor_env == "local":
            detected_resources = retrieve_computational_resources()
        else:
            ## TODO try to automate detection from scheduler?
            detected_resources = {"max_cpus": 4, "max_memory": 32}
        nfcore_resources = question_max_resources(detected_resources)
        nfcore_params.update(nfcore_resources)

    # Enable post run clean up
    cleanup_input = inquirer.prompt(
        [
            inquirer.Confirm(
                "cleanup",
                message="Do you want to enable cleanup of work directory on successful completion of a run? Note: this will break -resume!",
                default=False,
            )
        ]
    )["cleanup"]

    # Set NXF_TEMP if user wants 
    nxf_temp_question = [
        inquirer.Confirm(
            'set_nxf_temp',
            message="Do you want to specify a Nextflow temp directory (NXF_TEMP)?",
            default=False,
        )
    ]
    answers = inquirer.prompt(nxf_temp_question)

    if answers['set_nxf_temp']:
        # If user wants to specify NXF_TEMP, ask for the path
        nxf_temp_path_question = [
            inquirer.Text(
                'nxf_temp_path',
                message="Please enter the path for NXF_TEMP"
            )
        ]
        answers = inquirer.prompt(nxf_temp_path_question)
        nxf_temp_path = answers['nxf_temp_path']
    else:
        nxf_temp_path = None

    # Write preferences to custom config
    # TODO pass all relevant variables to this function
    write_config(
        cleanup_input,
        nxf_temp=nxf_temp_path,
        executor=scheduler_name,
        queue=queue_name,
        module_results=module_results,
        container=container_results,
        params=nfcore_params,
    )
