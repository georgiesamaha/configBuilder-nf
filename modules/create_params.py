#!/usr/bin/env python3

from colorama import Fore, Style, init
import inquirer
import subprocess
import psutil


def is_nfcore():
    nfcore_config_question = [
        inquirer.Confirm(
            "nfcore_question",
            message="Will this config be used for nf-core pipelines?",
            default=True,
        )
    ]
    return inquirer.prompt(nfcore_config_question)


## Config description
def question_config_owner():
    """
    Asks what the name and the github handle of the config creator, and also the institutional URL.

    This is for display in the official nf-core configs, and is useful for debugging
    """
    nfcore_question_name = [
        inquirer.Text(
            "nfcore_ownername",
            message="What is your name (full name preferred)?",
        )
    ]
    name_answer = inquirer.prompt(nfcore_question_name)
    param_ownername = name_answer["nfcore_ownername"]

    nfcore_question_handle = [
        inquirer.Text(
            "nfcore_ownerhandle",
            message="What is your GitHub handle? (optional)",
        )
    ]

    handle_answer = inquirer.prompt(nfcore_question_handle)
    param_ownerhandle = handle_answer["nfcore_ownerhandle"]

    nfcore_question_institute = [
        inquirer.Confirm(
            "nfcore_institutional",
            message="Is this config to be used on institutional infrastructure?",
            default=True,
        )
    ]

    institute_answer = inquirer.prompt(nfcore_question_institute)

    if institute_answer["nfcore_institutional"]:
        nfcore_question_url = [
            inquirer.Text(
                "nfcore_ownerurl",
                message="What is the URL of the institute? (optional)",
            )
        ]

        url_answer = inquirer.prompt(nfcore_question_url)
        param_ownerurl = url_answer["nfcore_ownerurl"]
    else:
        param_ownerurl = ""

    ## Construct final text for owner info
    if param_ownername != "" and param_ownerhandle != "":
        param_contact = (
            param_ownername + " (@" + param_ownerhandle.removeprefix("@") + ")"
        )
    elif param_ownername != "" and param_ownerhandle == "":
        param_contact = param_ownername
    elif param_ownername == "" and param_ownerhandle != "":
        param_contact = "@" + param_ownerhandle.removeprefix("@")
    else:
        param_contact = ""

    return {
        "config_profile_contact": param_contact,
        "config_profile_url": param_ownerurl,
    }

# Validate input is integer for max resources
def validate_integer(_, val):
    return val.isdigit()
## Resources information
def retrieve_computational_resources():
    """
    Pulls the total number of CPUs and memory of a given unix machine.

    Primarily designed for defining --max_cpus and --max_memory on single-machines.
    """
    cpu = psutil.cpu_count()
    memory = psutil.virtual_memory().total / 1024 / 1024 / 1024
    resources = {"max_cpus": cpu, "max_memory": memory}

    return resources


def question_max_resources(defaults):
    nfcore_question_maxcpus = [
        inquirer.Text(
            "nfcore_maxcpus",
            message="What is the maximum number of CPUs your infrastructure has available (e.g. on your machine, or the largest node accessible by all users of a HPC)?",
            default=defaults["max_cpus"],
        validate=validate_integer,
        )
    ]
    maxcpus = inquirer.prompt(nfcore_question_maxcpus)

    nfcore_question_maxmemory = [
        inquirer.Text(
            "nfcore_maxmemory",
            message="What is the maximum RAM that your infrastructure has available in GB (e.g. on your machine, or of the largest node accessible by all users of a HPC)?",
            default=int(round(defaults["max_memory"], 0)),
        validate=validate_integer,
        )
    ]
    maxmemory = inquirer.prompt(nfcore_question_maxmemory)

    nfcore_question_maxtime = [
        inquirer.Text(
            "nfcore_maxtime",
            message="What is the maximum walltime that your infrastructure has available in hours (e.g. of the largest node accessible by all users of a HPC)?",
            default="24",
        validate=validate_integer,
        )
    ]
    maxtime = inquirer.prompt(nfcore_question_maxtime)

    ## Include some input sanitisation to ensure correct suffix and no suffix duplicates
    return {
        "max_cpus": maxcpus["nfcore_maxcpus"],
        "max_memory": maxmemory["nfcore_maxmemory"].removeprefix(".GB") + ".GB",
        "max_time": maxtime["nfcore_maxtime"].removeprefix(".h") + ".h",
    }
