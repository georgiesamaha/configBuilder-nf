#!/usr/bin/env python3

from .create_params import is_nfcore, question_config_owner
from .create_hpc_env import check_scheduler, check_modules
from .write_config import write_config
from colorama import Fore, Style, init
import inquirer
from .create_container import create_container_scope

# Initialise colorama
init(autoreset=True)


def create_infrastructure():
    nfcore_config = is_nfcore()

    if nfcore_config:
        nfcore_params = question_config_owner()

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
    module_results = None  # Save name of module if found

    # Printing the selected environment
    print(f"You selected: {executor_env}.\n")

    # Infra-type specific options (in future could add cloud e.g. for AWS specific scopes)
    if executor_env == "hpc":
        scheduler_name = check_scheduler()
        module_results = check_modules()
        if scheduler_name != "none":
            print(f"The detected job scheduler is: {scheduler_name}.\n")
    else:
        pass

    print(Fore.YELLOW + "Checking for available software environment software...")
    container_results = create_container_scope()

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

    # Write preferences to custom config
    # TODO pass all relevant variables to this function
    write_config(
        cleanup_input,
        executor=scheduler_name,
        module_results=module_results,
        container=container_results,
        params=nfcore_params,
    )
