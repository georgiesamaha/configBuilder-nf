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

  # Define commands to detect schedulers 
  commands = {
    #'pbs' : 'qstat --version',
    'pbspro' : 'qstat --version',
    'sge' : 'qstat -help',
    'slurm' : 'sinfo --version'
  }

  # Test various scheduler help commands to identify which is running
  for scheduler, cmd in commands.items():
      try:
          #print(f"Trying {scheduler} with command: {cmd}")

          # Run the command and capture the output
          result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          output = result.stdout.decode('utf-8').strip()
          #print(f"Output for {scheduler}: {output}")

          if scheduler == 'pbspro' and 'pbs_version' in output:
              return 'pbspro'
          elif scheduler == 'sge' and 'usage: qstat' in output:
              return 'sge'
          elif scheduler == 'slurm' and result.returncode == 0:
              return 'slurm'
      except Exception as e:
          pass

def check_modules():
    """
    Check if a module system is being used on the HPC system. If so, load Singularity. Assumes HPC has Singularity. 
    """
    try:
        # Use subprocess to run the command within a shell context
        result = subprocess.run('module --version', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = result.stdout.decode('utf-8').strip()

        if "Modules Release" in output:
            print(Fore.GREEN + "Modules system detected.")
            
            result = subprocess.run('module avail', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            modules_available = result.stdout.decode('utf-8').strip()

            if "singularity" in modules_available:
                print(Fore.GREEN + "Singularity module is available.")
                return {"singularity": True}
                
            else:
                print(Fore.YELLOW + "Singularity module is not available.")
            return True
            return {"singularity": False}

        else:
            print(Fore.YELLOW + "No modules system detected.")
            return False
    except Exception as e:
        print(Fore.RED + "Error checking for modules system: " + str(e))
        return False
