#!/usr/bin/env python3

from colorama import Fore, Style, init
import inquirer
import os

# Initialise colorama
init(autoreset=True)


def write_config(cleanup_input, executor, queue, container, params=None, module_results=None):
    """
    Write the user's specifications to variables inside the config template below and output to a text file.
    """
    # Prompt user for custom config name
    output_file = inquirer.prompt(
        [
            inquirer.Text(
                "output_file",
                message="What is the name of the config?",
                default="custom_nextflow",
            )
        ]
    )["output_file"]

    with open(output_file.replace(" ", "_") + ".config", "w") as f:
        f.write("// Custom config file for " + output_file + "\n\n")

        if params:
            if not all([i == "" for i in list(params.values())]):
                for i in params:
                    if params[i] != "":
                        f.write("params." + i + " = " + params[i] + "\n")
                f.write("\n")

        if executor != "none":
            f.write("process {\n")
            f.write(f"    executor = '{executor}'\n")
            f.write(f"    queue = '{queue}'\n")
            f.write("}\n\n")

        if container is not False:
            f.write(container["container_options"] + ".enabled = true\n")
            if container["container_options"] in ["singularity", "apptainer"]:
                f.write(container["container_options"] + ".autoMounts = true\n")

        if cleanup_input:
            f.write("cleanup = true\n")
