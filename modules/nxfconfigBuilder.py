from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def nxfconfigBuilder():
    def ask_for_input(prompt, type_=None, min_=None, max_=None, num_of_attempts=3):
        for _ in range(num_of_attempts):
            val = input(Fore.GREEN + prompt + Style.RESET_ALL)
            if type_ is not None:
                try:
                    val = type_(val)
                except ValueError:
                    print(Fore.RED + f"Input type must be {type_.__name__}!" + Style.RESET_ALL)
                    continue
            if min_ is not None and val < min_:
                print(Fore.RED + f"Input must be greater than or equal to {min_}!" + Style.RESET_ALL)
            elif max_ is not None and val > max_:
                print(Fore.RED + f"Input must be less than or equal to {max_}!" + Style.RESET_ALL)
            else:
                return val
        raise ValueError('Invalid Input')

    # Set defaults
    queue = None
    module = 'nextflow'
    clusterOptions = ''

    executor = input(Fore.MAGENTA + "What executor does your system use (default is 'local')? " + Style.RESET_ALL)
    executor = executor if executor else 'local'

    # Nextflow supported job schedulers: https://www.nextflow.io/docs/latest/executor.html 
    if executor in ['pbspro', 'slurm', 'azure batch', 'aws batch', 'bridge', 'flux', 'lsf', 'moab', 'oar', 'nqsii', 'pbs', 'sge']:
        
        # Enter queue to run processes on
        queue = input(Fore.MAGENTA + "What queue would you like to run your jobs on? " + Style.RESET_ALL)
    
        # Define modules to run before executing workflow processes 
        module = input(Fore.MAGENTA + "What modules and versions should be loaded before executing each process (default is 'nextflow')? " + Style.RESET_ALL)
        module = module if module else 'nextflow'

        # Define any cluster options that need to be applied 
        clusterOptions = input(Fore.MAGENTA + "What cluster options should be applied to each process execution (e.g. -P <projectname>)? " + Style.RESET_ALL)

    # Enter number of CPUs available on the queue
    cpus = ask_for_input(Fore.MAGENTA + "What is the max number of CPUs available on this queue (default is 1)? ", type_=int, min_=1)
    cpus = cpus if cpus else 1

    # Enter the amount of memory available on the queue 
    memory = ask_for_input(Fore.MAGENTA + "What is the max amount of memory in GB available on this queue (default is 1)? ", type_=int, min_=1)
    memory = memory if memory else 1

    # Enter the maxiumum walltime for the queue 
    # See: https://www.nextflow.io/docs/latest/process.html?highlight=cpus#time
    walltime = ask_for_input(Fore.MAGENTA + "What is the max walltime available on this queue (default is 0.5h)? ", type_=float, min_=0.5)
    walltime = walltime if walltime else 0.5
    
    # Name custom config file
    output_file = input(Fore.YELLOW + "Enter the output file name (default is 'custom_nextflow.config'): " + Style.RESET_ALL)
    output_file = output_file if output_file else 'custom_nextflow.config'

    with open(output_file, 'w') as f:
        f.write("// Custom Nextflow config file \n\n")
        f.write("process {\n")
        f.write(f"    executor = '{executor}'\n")
        if queue:
            f.write(f"    queue = '{queue}'\n")
        if module:
            f.write(f"    beforeScript = 'module load {module}'\n")
        if clusterOptions:
            f.write(f"    clusterOptions = '{clusterOptions}'\n")
        f.write(f"    cpus = {cpus}\n")
        f.write(f"    memory = '{memory}GB'\n")
        f.write(f"    time = '{walltime}h'\n")
        f.write("}\n\n")

