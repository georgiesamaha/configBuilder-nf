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

    executor = input(Fore.MAGENTA + "What executor does your system use (default is 'local')? \nFor more information, see https://www.nextflow.io/docs/latest/executor.html \n" + Style.RESET_ALL)
    executor = executor if executor else 'local'

    if executor in ['pbspro', 'slurm', 'azure batch', 'aws batch', 'bridge', 'flux', 'lsf', 'moab', 'oar', 'nqsii', 'pbs', 'sge']:
        queue = input(Fore.MAGENTA + "What queue would you like to run your jobs on? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#queue \n" + Style.RESET_ALL)
        module = input(Fore.MAGENTA + "What modules and versions should be loaded before executing each process (default is 'nextflow')? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#beforescript \n" + Style.RESET_ALL)
        module = module if module else 'nextflow'
        clusterOptions = input(Fore.MAGENTA + "What cluster options should be applied to each process execution? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#clusteroptions \n" + Style.RESET_ALL)

    cpus = ask_for_input(Fore.MAGENTA + "What is the max number of CPUs available on this queue (default is 1)? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#cpus \n", type_=int, min_=1)
    cpus = cpus if cpus else 1
    memory = ask_for_input(Fore.MAGENTA + "What is the max amount of memory in GB available on this queue (default is 1)? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#memory \n", type_=int, min_=1)
    memory = memory if memory else 1
    walltime = ask_for_input(Fore.MAGENTA + "What is the max walltime available on this queue (default is 0.5h)? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#time \n", type_=float, min_=0.5) if executor in ['pbspro', 'slurm', 'azure batch', 'aws batch', 'bridge', 'flux', 'lsf', 'moab', 'oar', 'nqsii', 'pbs', 'sge'] else None
    walltime = walltime if walltime else 0.5

    # Use withName selector to specify process-specific resources
    process_specific_configs = []
    while True:
        add_process_specific_config = input(Fore.CYAN + "Do you want to specify unique resource needs for a particular process? (yes/no) " + Style.RESET_ALL)
        if add_process_specific_config.lower() == 'yes':
            process_name = input(Fore.YELLOW + "Please enter the process name: " + Style.RESET_ALL)
            process_executor = input(Fore.MAGENTA + f"What executor should this process use (default is '{executor}')? " + Style.RESET_ALL)
            process_executor = process_executor if process_executor else executor
            process_cpus = ask_for_input(Fore.MAGENTA + "What is the max number of CPUs for this process (default is 1)? ", type_=int, min_=1)
            process_memory = ask_for_input(Fore.MAGENTA + "What is the max amount of memory in GB for this process (default is 1)? ", type_=int, min_=1)
            process_walltime = ask_for_input(Fore.MAGENTA + "What is the max walltime for this process (default is 0.5h)? ", type_=float, min_=0.5) if process_executor == executor else None
            process_walltime = process_walltime if process_walltime else 0.5
            process_queue = input(Fore.MAGENTA + "What queue should this process run on? " + Style.RESET_ALL) if process_executor == executor else None
            
            process_specific_configs.append({
                'name': process_name,
                'executor': process_executor,
                'cpus': process_cpus,
                'memory': process_memory,
                'walltime': process_walltime,
                'queue': process_queue
            })
        elif add_process_specific_config.lower() == 'no':
            break
        else:
            print(Fore.RED + "Invalid input! Please enter 'yes' or 'no'." + Style.RESET_ALL)
    
    # Write outputs to custom configuration file
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
        if walltime is not None:
            f.write(f"    time = '{walltime}h'\n")
        for config in process_specific_configs:
            f.write(f"    \nwithName: {config['name']} {{\n")
            f.write(f"        executor = '{config['executor']}'\n")
            if config['queue']:
                f.write(f"        queue = '{config['queue']}'\n")
            f.write(f"        cpus = {config['cpus']}\n")
            f.write(f"        memory = '{config['memory']}GB'\n")
            if config['walltime'] is not None:
                f.write(f"        time = '{config['walltime']}h'\n")
            f.write("    }\n")
        f.write("}\n\n")