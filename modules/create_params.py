#!/usr/bin/env python3

from colorama import Fore, Style, init
import inquirer
import subprocess


def is_nfcore():
    nfcore_config_question = [
        inquirer.Confirm(
            "nfcore_question",
            message="Will this config be used for nf-core pipelines?",
            default=True,
        )
    ]
    return inquirer.prompt(nfcore_config_question)


def question_config_owner():
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
