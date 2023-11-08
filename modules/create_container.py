#!/usr/bin/env python3

import subprocess
import os
import inquirer
from colorama import Fore, Style, init
from .utilities import create_tool_options

## TODO: consider how to address `module` environment detection here

nxf_software_management = (
    "conda",
    "docker",
    "singularity",
    "apptainer",
    "charliecloud",
    "podman",
    "sarus",
    "shifter",
)


def detect_containers(options=nxf_software_management):
    container_options = create_tool_options(options)

    return container_options


container_options = detect_containers()


def create_container_scope(options=container_options):
    if not container_options:
        print(Fore.YELLOW + "...no software environment systems detected.")
        question = [
            inquirer.Confirm(
                "container_manual_selection",
                message="Would you like to manually select a software environment?",
            )
        ]
        manual_question = inquirer.prompt(question)

        if manual_question["container_manual_selection"]:
            question = [
                inquirer.List(
                    "container_options",
                    message="Which software environment system would you like to use?",
                    choices=nxf_software_management,
                )
            ]
            answer = inquirer.prompt(question)
        else:
            answer = False
    else:
        print(
            Fore.YELLOW
            + "..."
            + str(len(container_options))
            + " software environment systems detected."
        )
        question = [
            inquirer.List(
                "container_options",
                message="Which software environment system would you like to use?",
                choices=options,
            )
        ]
        answer = inquirer.prompt(question)

    return answer
