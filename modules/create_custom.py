#!/usr/bin/env python3
from .create_hpc_env import check_scheduler, check_modules
from colorama import Fore, Style, init
import inquirer

# Initialise colorama
init(autoreset=True)

def custom_pipeline():

    execution_env_question = [
    inquirer.List('executor_env', 
                message="What type of execution environment are you working in?",
                choices= ['hpc', 'local', 'cloud'],
                ),
    ]
    answers = inquirer.prompt(execution_env_question)
    executor_env = answers['executor_env']

    scheduler_name = None  # This will store the name of the detected scheduler if 'hpc' is chosen

    if executor_env == "hpc":
        scheduler_name = check_scheduler()
    elif executor_env == "local":
        create_local_env()
    elif executor_env == "cloud":
        create_cloud_env()

    # Printing the selected environment
    print(f"You selected: {executor_env}")

    # If 'hpc' was chosen, also print the detected scheduler
    if scheduler_name:
        print(f"The detected job scheduler is: {scheduler_name}")

    # Inform the user that it's checking for the Singularity module
        print(f"Checking HPC for Singularity module to run containers.")
        check_modules()

    # TODO add message for if local was chosen 
    # TODO add message for if cloud was chosen