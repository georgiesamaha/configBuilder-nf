from colorama import Fore, Style, init
import inquirer

# Initialise colorama
init(autoreset=True)


def nfconfigBuilder():
    # Set default values for required inputs
    queue = None
    module = "nextflow"
    clusterOptions = ""

    # Ask which nf-core pipeline this is built for
    pipeline_question = [
        inquirer.Text("pipeline", message="Which nf-core pipeline are you using?")
    ]

    pipeline_answer = inquirer.prompt(pipeline_question)
    pipeline = pipeline_answer["pipeline"]

    print(f"You are using the {pipeline} pipeline.")

    # Define executor, can only be one supported by Nextflow
    executor_list = [
        "local",
        "aws batch",
        "azure batch",
        "bridge",
        "flux",
        "lsf",
        "moab",
        "nqsii",
        "oar",
        "pbs",
        "pbspro",
        "sge",
        "slurm",
    ]

    questions = [
        inquirer.List(
            "executor",
            message="Select the job scheduler that your HPC system uses (Specify local to run jobs on login node)",
            choices=executor_list,
        ),
    ]

    answers = inquirer.prompt(questions)
    executor = answers["executor"]

    print(f"You selected: {executor}")

    # Define queue, modules and clusterOptions
    questions = [
        inquirer.Text(
            "module",
            message="Enter modules and versions should be loaded before executing each process? (separate multiple modules by a space)",
            default="nextflow",
        ),
    ]
    if executor != "local":
        questions.extend(
            [
                inquirer.Text(
                    "queue",
                    message="Specify the queue you would like to run your jobs on",
                ),
                inquirer.Text(
                    "clusterOptions",
                    message="Specify cluster options that should be applied to each process",
                ),
            ]
        )
    answers = inquirer.prompt(questions)
    module = answers.get("module", "nextflow")
    queue = answers.get("queue")
    clusterOptions = answers.get("clusterOptions")

    # Define compute resource limits regardless of if local or executor
    cpus = inquirer.prompt(
        [
            inquirer.Text(
                "cpus",
                message="Specify the max number of CPUs to be allocated to each process",
                default="1",
                validate=lambda _, x: x.isdigit(),
            )
        ]
    )["cpus"]
    memory = inquirer.prompt(
        [
            inquirer.Text(
                "memory",
                message="Specify the max amount of memory in GB to be allocated to each process",
                default="1",
                validate=lambda _, x: x.isdigit(),
            )
        ]
    )["memory"]
    walltime = (
        inquirer.prompt(
            [
                inquirer.Text(
                    "walltime",
                    message="Specify the max walltime in hours for each process",
                    default="0.5",
                    validate=lambda _, x: x.replace(".", "", 1).isdigit(),
                )
            ]
        )["walltime"]
        if executor in executor_list
        else None
    )

    # Use withLabel selector to specify label-specific resources
    label_specific_configs = []
    while True:
        add_label_specific_config = inquirer.prompt(
            [
                inquirer.List(
                    "add_label_specific_config",
                    message="Do you want to specify unique resource needs for a particular label?",
                    choices=["yes", "no"],
                )
            ]
        )["add_label_specific_config"]
        if add_label_specific_config.lower() == "yes":
            questions = [
                inquirer.Text("label_name", message="Please enter the label name"),
                inquirer.List(
                    "label_executor",
                    message="Specify the executor this label should use",
                    choices=executor_list,
                    default=executor,
                ),
            ]
            answers = inquirer.prompt(questions)
            if answers["label_executor"] != "local":
                queue_answer = inquirer.prompt(
                    [
                        inquirer.Text(
                            "label_queue",
                            message="Specify the queue this label should use",
                        )
                    ]
                )
                answers["label_queue"] = queue_answer["label_queue"]
            label_specific_configs.append(answers)
        elif add_label_specific_config.lower() == "no":
            break

    # Use withName selector to specify process-specific resources
    process_specific_configs = []
    while True:
        add_process_specific_config = inquirer.prompt(
            [
                inquirer.List(
                    "add_process_specific_config",
                    message="Do you want to specify unique resource needs for a particular process?",
                    choices=["yes", "no"],
                )
            ]
        )["add_process_specific_config"]
        if add_process_specific_config.lower() == "yes":
            questions = [
                inquirer.Text("process_name", message="Please enter the process name"),
                inquirer.List(
                    "process_executor",
                    message="Specify the executor this process should use",
                    choices=executor_list,
                    default=executor,
                ),
                inquirer.Text(
                    "process_cpus",
                    message="Specify the max number of CPUs to be allocated to each process",
                    default="1",
                    validate=lambda _, x: x.isdigit(),
                ),
                inquirer.Text(
                    "process_memory",
                    message="Specify the max amount of memory in GB to be allocated to each process",
                    default="1",
                    validate=lambda _, x: x.isdigit(),
                ),
                inquirer.Text(
                    "process_walltime",
                    message="Specify the max walltime in hours for each process",
                    default="0.5",
                    validate=lambda _, x: x.replace(".", "", 1).isdigit(),
                )
                if executor in executor_list
                else None,
            ]
            answers = inquirer.prompt(questions)

            if answers["process_executor"] != "local":
                queue_answer = inquirer.prompt(
                    [
                        inquirer.Text(
                            "process_queue",
                            message="Specify the queue this process should use",
                        )
                    ]
                )
                answers["process_queue"] = queue_answer["process_queue"]

            process_specific_configs.append(answers)
        elif add_process_specific_config.lower() == "no":
            break

    # Write outputs to custom configuration file
    output_file = inquirer.prompt(
        [
            inquirer.Text(
                "output_file",
                message="Enter the custom config name",
                default="custom_nfcore.config",
            )
        ]
    )["output_file"]

    with open(output_file, "w") as f:
        f.write(f"// Custom nf-core/{pipeline} config file \n\n")
        f.write("process {\n")
        if module:
            f.write(f"    beforeScript = 'module load {module}'\n")
        f.write(f"    executor = '{executor}'\n")
        if queue:
            f.write(f"    queue = '{queue}'\n")
        if clusterOptions:
            f.write(f"    clusterOptions = '{clusterOptions}'\n")
        f.write(f"    cpus = {cpus}\n")
        f.write(f"    memory = '{memory}GB'\n")
        if walltime is not None:
            f.write(f"    time = '{walltime}h'\n")
        for config in label_specific_configs:
            f.write(f"\n    withLabel: {config['label_name']} {{\n")
            f.write(f"        executor = '{config['label_executor']}'\n")
            if config.get("label_queue"):
                f.write(f"        queue = '{config['label_queue']}'\n")
            f.write(f"    }}\n")
        for config in process_specific_configs:
            f.write(f"\n    withName: {config['process_name']} {{\n")
            f.write(f"        executor = '{config['process_executor']}'\n")
            if config.get("process_queue"):
                f.write(f"        queue = '{config['process_queue']}'\n")
            f.write(f"        cpus = {config['process_cpus']}\n")
            f.write(f"        memory = '{config['process_memory']}GB'\n")
            if config.get("process_walltime") is not None:
                f.write(f"        time = '{config['process_walltime']}h'\n")
            f.write(f"    }}\n")
        f.write(f"}}\n")

    print(
        f"{Fore.GREEN}Config file {output_file} has been successfully created!{Style.RESET_ALL}"
    )
