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
        print(f"You selected: {cont_answer['container_options']}.\n")

    cach_question = [
        inquirer.Confirm(
            "cachedir_manual_selection",
            message="Would you like to use a software environment cache directory?",
            default=True,
        )
    ]
    manual_cach_question = inquirer.prompt(cach_question)

    if manual_cach_question["cachedir_manual_selection"]:
        print(
            Fore.YELLOW
            + "Checking for existing cache directories of selected software environment or container engine..."
        )

        try:
            cache_detection_results = nxf_software_cachedirs[
                cont_answer["container_options"]
            ]
            detected_cache = cach_options[cache_detection_results]
            print(
                Fore.YELLOW
                + "...a software environment cache directory was detected!\n"
            )
        except KeyError as e:
            print(
                Fore.YELLOW
                + "...no existing software environment cache directory was found.\n"
            )
            detected_cache = None

        if detected_cache is not None:
            ## Ask if they want the detected cache, and if yes, return it
            cach_detected_question = [
                ## Ugly hack to pull the actual directory path, but I'm tired.
                inquirer.Confirm(
                    "cachedir_confirm_detected",
                    message="Would you like to re-use the detected cache directory: "
                    + cache_options[
                        nxf_software_cachedirs[cont_answer["container_options"]]
                    ]
                    + "?",
                    default=True,
                )
            ]
            detected_cach_question = inquirer.prompt(cach_detected_question)
            if detected_cach_question["cachedir_confirm_detected"]:
                cach_answer = detected_cache
            else:
                ## If they don't want the detected cache, ask for a new one
                cach_selection_question = [
                    inquirer.Text(
                        "cachedir_options",
                        message="Please specify the directory you wish to cache environments or images (must exist).",
                        validate=check_dir_exists,
                    )
                ]
                manual_cach_answer = inquirer.prompt(cach_selection_question)
                cach_answer = manual_cach_answer["cachedir_options"]
                print(f"You selected: {cach_answer}.\n")
        else:
            ## If we don't detect a cache, ask for a new one
            cach_selection_question = [
                inquirer.Text(
                    "cachedir_options",
                    message="Please specify the directory you wish to cache environments or images (must exist).",
                    validate=check_dir_exists,
                )
            ]
            manual_cach_answer = inquirer.prompt(cach_selection_question)
            cach_answer = manual_cach_answer["cachedir_options"]
            print(f"You selected: {cach_answer}.\n")
    else:
        cach_answer = None

    return cont_answer
