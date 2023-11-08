#!/usr/bin/env python3

from .create_hpc_env import check_scheduler, check_modules
from .write_config import write_config
from colorama import Fore, Style, init
import inquirer
from .create_container import create_container_scope

# Initialise colorama
init(autoreset=True)


def create_infrastructure():
    execution_env_question = [
        inquirer.List(
            "executor_env",
            message="What type of execution environment are you working in?",
            choices=["hpc", "local", "cloud"],
        ),
    ]
    answers = inquirer.prompt(execution_env_question)
    executor_env = answers["executor_env"]

    scheduler_name = None  # Save name of scheduler if hpc selected
    module_results = None  # Save name of module if found

    # Printing the selected environment
    print(f"You selected: {executor_env}")

    # Infra-type specific options (in future could add cloud e.g. for AWS specific scopes)
    if executor_env == "hpc":
        scheduler_name = check_scheduler()
        module_results = check_modules()
        if scheduler_name != "none":
            print(f"The detected job scheduler is: {scheduler_name}")
    else:
        pass

    print(Fore.YELLOW + "Checking for available software environment software...")
    container_results = create_container_scope()

    # Write preferences to custom config
    # TODO pass all relevant variables to this function
    write_config(
        executor=scheduler_name,
        module_results=module_results,
        container=container_results,
    )
