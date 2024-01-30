#!/usr/bin/env python3

import subprocess
import os
import inquirer
from colorama import Fore, Style, init
from .utilities import create_tool_options, create_cachedir_options, check_dir_exists

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

nxf_software_cachedirs = [
    "NXF_CHARLIECLOUD_CACHEDIR",
    "NXF_CONDA_CACHEDIR",
    "NXF_SINGULARITY_CACHEDIR",
    "NXF_APPTAINER_CACHEDIR",
]


## TODO: extend to instead use module detection system if available
def detect_containers(options=nxf_software_management):
    container_options = create_tool_options(options)

    return container_options


container_options = detect_containers()


def detect_cachedirs(options=nxf_software_cachedirs):
    cachedir_options = create_cachedir_options(options)
    return cachedir_options


cachedir_options = detect_cachedirs()


def create_container_scope(
    cont_options=container_options, cach_options=cachedir_options
):
    if not cont_options:
        print(Fore.YELLOW + "...no software environment systems detected.\n")
        cont_question = [
            inquirer.Confirm(
                "container_manual_selection",
                message="Would you like to manually select a software environment?",
            )
        ]
        manual_cont_question = inquirer.prompt(cont_question)

        if manual_cont_question["container_manual_selection"]:
            cont_selection_question = [
                inquirer.List(
                    "container_options",
                    message="Which software environment system would you like to use?",
                    choices=nxf_software_management,
                )
            ]
            cont_answer = inquirer.prompt(cont_selection_question)
        else:
            cont_answer = False
    else:
        print(
            Fore.YELLOW
            + "..."
            + str(len(container_options))
            + " software environment systems detected.\n"
        )
        cont_selection_question = [
            inquirer.List(
                "container_options",
                message="Which software environment system would you like to use?",
                choices=cont_options,
            )
        ]
        cont_answer = inquirer.prompt(cont_selection_question)

    if not cach_options:
        print(Fore.YELLOW + "...no software environment cache directories detected.\n")
        cach_question = [
            inquirer.Confirm(
                "cachedir_manual_selection",
                message="Would you like to manually specify a software environment cache directory?",
            )
        ]
        manual_cach_question = inquirer.prompt(cach_question)

        if manual_cach_question["cachedir_manual_selection"]:
            cach_selection_question = [
                inquirer.Text(
                    "cachedir_options",
                    message="Please specify the directory you wish to cache environments or images (must exist).",
                    validate=check_dir_exists,
                )
            ]
            cach_answer = inquirer.prompt(cach_selection_question)
        else:
            cach_answer = False
    else:
        print(
            Fore.YELLOW
            + "..."
            + str(len(container_options))
            + " software environment systems detected.\n"
        )
        cach_selection_question = [
            inquirer.List(
                "container_options",
                message="Which software environment system would you like to use?",
                choices=cach_options,
            )
        ]
        cont_answer = inquirer.prompt(cach_selection_question)

    return [cont_answer, cach_answer]
