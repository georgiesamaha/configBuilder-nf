#!/usr/bin/env python3

import subprocess
import os
import inquirer
from colorama import Fore, Style, init
from .utilities import create_tool_options

nxf_software_management = (
    "conda",
    "docker",
    "singularity",
    "charliecloud",
    "podman",
    "sarus",
    "shifter",
    "apptainer",
)


def detect_containers(options=nxf_software_management):
    container_options = create_tool_options(options)

    return container_options


## TODO: account for nothing found
container_options = detect_containers()


def create_container_scope(options=container_options):
    question = [
        inquirer.List(
            "container_options",
            message="Which software environment system would you like to use?",
            choices=options,
        )
    ]
    inquirer.prompt(question)
