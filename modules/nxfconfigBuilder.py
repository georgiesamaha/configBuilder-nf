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
        queue = input(Fore.MAGENTA + "What queue would you like to run your jobs on? For more information, see https://www.nextflow.io/docs/latest/process.html#queue \n" + Style.RESET_ALL)
        module = input(Fore.MAGENTA + "What modules and versions should be loaded before executing each process (default is 'nextflow')? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#beforescript \n" + Style.RESET_ALL)
        module = module if module else 'nextflow'
        clusterOptions = input(Fore.MAGENTA + "What cluster options should be applied to each process execution (e.g. -P <projectname>)? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#clusteroptions \n" + Style.RESET_ALL)

    cpus = ask_for_input(Fore.MAGENTA + "What is the max number of CPUs available on this queue (default is 1)? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#cpus \n", type_=int, min_=1)
    cpus = cpus if cpus else 1
    memory = ask_for_input(Fore.MAGENTA + "What is the max amount of memory in GB available on this queue (default is 1)? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#memory \n", type_=int, min_=1)
    memory = memory if memory else 1
    walltime = ask_for_input(Fore.MAGENTA + "What is the max walltime available on this queue (default is 0.5h)? \nFor more information, see https://www.nextflow.io/docs/latest/process.html#time \n", type_=float, min_=0.5)
    walltime = walltime if walltime else 0.5
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
