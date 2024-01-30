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

nxf_software_cachedirs = {
    "charliecloud": "NXF_CHARLIECLOUD_CACHEDIR",
    "conda": "NXF_CONDA_CACHEDIR",
    "singularity": "NXF_SINGULARITY_CACHEDIR",
    "apptainer": "NXF_APPTAINER_CACHEDIR",
}


## TODO: extend to instead use module detection system if available
def detect_containers(options=nxf_software_management):
    container_options = create_tool_options(options)
    return container_options


container_options = detect_containers()


def detect_cachedirs(options=nxf_software_cachedirs):
    cachedir_options = create_cachedir_options(options)
    return cachedir_options


cache_options = detect_cachedirs()


def create_container_scope(cont_options=container_options, cach_options=cache_options):
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

    cach_question = [
        inquirer.Confirm(
            "cachedir_manual_selection",
            message="Would you like to manually specify a software environment cache directory?",
        )
    ]
    manual_cach_question = inquirer.prompt(cach_question)

    if manual_cach_question["cachedir_manual_selection"]:
        print(
            Fore.YELLOW
            + "Checking for existing cache directories of selected software environment or container engine..."
        )
        cache_detection_results = nxf_software_cachedirs[
            cont_answer["container_options"]
        ]
        detected_cache = cach_options[cache_detection_results]

        ## TODO Print message whether result has been found or not, then ask if user is happy

    ## TODO: NEW STRUCTURE

    ## Q: Would you like to use a cache?
    ##      If yes
    ##          AUTODETECT CACHE NOW OR SAY SEARCHING
    ##          Based on your env/software selection, we detected the following, would you like you use it? (default: detected)
    ##              If yes:
    ##                  cache_answer = result
    ##              If no:
    ##                  Please specify a new cache location (+ validate)
    ##                  cache_answer = result
    ##      If no
    ##          cache_answer = False

    # if not cach_options:
    #     print(Fore.YELLOW + "...no software environment cache directories detected.\n")
    #     cach_question = [
    #         inquirer.Confirm(
    #             "cachedir_manual_selection",
    #             message="Would you like to manually specify a software environment cache directory?",
    #         )
    #     ]
    #     manual_cach_question = inquirer.prompt(cach_question)

    #     if manual_cach_question["cachedir_manual_selection"]:
    #         cach_selection_question = [
    #             inquirer.Text(
    #                 "cachedir_options",
    #                 message="Please specify the directory you wish to cache environments or images (must exist).",
    #                 validate=check_dir_exists,
    #             )
    #         ]
    #         cach_answer = inquirer.prompt(cach_selection_question)
    #     else:
    #         cach_answer = False

    return [cont_answer, cach_answer]
