#!/usr/bin/env python3
from colorama import Fore, Style, init
import inquirer
import subprocess

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
  Check if a module system is being run on HPC system. If so, what modules should be loaded? 
  """