#!/usr/bin/env python

import os
import sys
import subprocess


def check_tool_on_path(tool):
    """
    Simply checks that by running the name of the tool in a shell, that the shell does not return an exit code of 127 (i.e., 'not found' error).
    """
    status = subprocess.getstatusoutput(tool)
    result = (
        status[0] != 127
    )  ## 127 means not found, everything else implies exists, we make assumption it's working
    return result


def check_var_in_env(var):
    """
    Simply checks that an variable exists in the environment
    """
    status = os.getenv(var)
    result = status  ## 127 means not found, everything else implies exists, we make assumption it's working
    return result


def create_tool_options(options):
    """
    Produces a list of 'valid' entries in a set, i.e., when running check_tool_on_path it will keep everything that has been evaluated to true.

    This reduced list can then be used to offer 'valid' options to the user.
    """
    available = set()
    for i in options:
        if check_tool_on_path(i):
            available.add(i)
    return available


def create_cachedir_options(options):
    """
    Produces a list of 'valid' entries in a set, i.e., when running check_tool_on_path it will keep everything that has been evaluated to true.

    This reduced list can then be used to offer 'valid' options to the user.
    """
    available = set()
    for i in options:
        if check_var_in_env(i):
            available.add(i)
    return available
