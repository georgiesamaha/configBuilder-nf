#!/usr/bin/env python3

from .create_hpc_env import check_scheduler, check_modules
from .write_config import write_config
from colorama import Fore, Style, init
import inquirer

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

    # Printing the selected environment
    print(f"You selected: {executor_env}")

    if executor_env == "hpc":
        scheduler_name = check_scheduler()
        module_results = check_modules()
    elif executor_env == "local":
        create_local_env()
    elif executor_env == "cloud":
        create_cloud_env()

    # If hpc, state scheduler found
    if scheduler_name != "none":
        print(f"The detected job scheduler is: {scheduler_name}")

    # Check for singularity
    if module_results:
        print(f"Enabling Singularity to execute containers")

    # TODO add message for if local was chosen
    # TODO add message for if cloud was chosen

    # Write preferences to custom config
    # TODO pass all relevant variables to this function
    write_config(executor=scheduler_name, module_results=module_results)
