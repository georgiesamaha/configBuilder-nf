#!/usr/bin/env python3

from colorama import Fore, Style, init
import inquirer
import os

# Initialise colorama
init(autoreset=True)


def write_config(executor, module_results=None):
    """
    Write the user's specifications to variables inside the config template below and output to a text file.
    """
    # Prompt user for custom config name
    output_file = inquirer.prompt(
        [
            inquirer.Text(
                "output_file",
                message="What do you want your custom config file to be called?",
                default="custom_nextflow.config",
            )
        ]
    )["output_file"]

    with open(output_file, "w") as f:
        f.write("// Custom Nextflow config file \n\n")
        print(module_results)
        if module_results.get("singularity"):
            f.write("singularity {\n")
            f.write("    enabled = true\n")
            # f.write(f"    NXF_SINGULARITY_CACHEDIR = {singularity_cache} \n")
        f.write("}\n\n")

        f.write("process {\n")
        f.write(f"    executor = '{executor}'\n")
        f.write("}\n\n")
