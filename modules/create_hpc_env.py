#!/usr/bin/env python3

from colorama import Fore, Style, init
import inquirer
import subprocess
import os

# Initialise colorama
init(autoreset=True)


def check_scheduler():
    """
    Check which scheduler is running on the system. Return the name of the scheduler to be printed to the custom config executor directive.
    """
    print(Fore.YELLOW + "Checking for available schedulers...")
    # Define commands to detect schedulers
    commands = {
        #'pbs' : 'qstat --version',
        # TODO: work out way to differentiate pbs and pbs pro
        "pbspro": "qstat --version",
        "sge": "qstat -help",
        "slurm": "sinfo --version",
    }

    detected_scheduler = "none"

    # Test various scheduler help commands to identify which is running
    for scheduler, cmd in commands.items():
        try:
            # print(f"Trying {scheduler} with command: {cmd}")

            # Run the commands and capture the output
            result = subprocess.run(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output = result.stdout.decode("utf-8").strip()
            # print(f"Output for {scheduler}: {output}")

            if scheduler == "pbspro" and "pbs_version" in output:
                detected_scheduler = "pbspro"
            elif scheduler == "sge" and "qstat" in output:
                detected_scheduler = "sge"
            elif scheduler == "slurm" and result.returncode == 0:
                detected_scheduler = "slurm"

        except Exception as e:
            detected_scheduler = "none"

    if detected_scheduler == "none":
        print(Fore.YELLOW + "...no scheduling system detected.\n")

    return detected_scheduler

def check_queues(detected_scheduler):
    """
    Detect available job queues for auto-detected scheduler (SGE, PBSpro, SLURM). 
    """
    detected_queues = "none" 
    print(Fore.YELLOW + "Checking for available queues...\n")
    
    if detected_scheduler == "pbspro":
        cmd = "qstat -Q"
        result = subprocess.run(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        output = result.stdout.decode("utf-8").strip()
        detected_queues = [line.split()[0] for line in output.split('\n')[2:] if line.strip()]

        if detected_queues:
            print(Fore.GREEN + "Found queues...")

            # Prompt user to select a queue
            queue_question = [
                inquirer.List(
                    "selected_queue",
                    message="Which queue do you want to execute your processes?",
                    choices=detected_queues
                )
            ]
            answers = inquirer.prompt(queue_question)
            selected_queue = answers["selected_queue"]

            print("Selected queue:", selected_queue)
            return selected_queue
        else:
            print(Fore.YELLOW + "No queues found.")
        #print(Fore.GREEN + "Queues: {detected_queues} detected.\n")
    return detected_queues

def check_modules():
    """
    Check if a module system is being used on the HPC system. If so, load Singularity. Assumes HPC has Singularity.
    """
    print(Fore.YELLOW + "Checking if a module environment system is present...")
    try:
        # Run module --version to see if its installed
        result = subprocess.run(
            "module --version",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        output = result.stdout.decode("utf-8").strip()

        if "Modules Release" in output:
            print(Fore.GREEN + "Modules system detected.\n")

            result = subprocess.run(
                "module avail",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            modules_available = result.stdout.decode("utf-8").strip()

            if "singularity" in modules_available:
                print(Fore.GREEN + "Singularity module is available.")
                return {"singularity": True}

            else:
                print(Fore.YELLOW + "Singularity module is not available.")
            return True
            return {"singularity": False}

        else:
            print(Fore.YELLOW + "...no modules system detected.\n")
            return {"not_detected": True}

    except Exception as e:
        print(Fore.RED + "Error checking for modules system: " + str(e))
        return False