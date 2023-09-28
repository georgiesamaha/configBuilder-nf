# configBuilder-nf: Nextflow configs for HPC

configBuilder-nf is a Python-based application for building custom configuration files for running your Nextflow and nf-core pipelines for High Performance Computing (HPC) infrastructures. This tool uses command-line prompts to collect specific details from you regarding the HPC job scheduler your system works with, compute resources available to you, and more. The collected inputs are then formatted and written to a configuration file, making it easier for uses to deploy pipelines on HPC infrastructures.

## Installation 

To run this application you will need to have Python3 installed and the following Python packages: 

* [colorama](https://pypi.org/project/colorama/)
* [inquirer](https://pypi.org/project/inquirer/)

1. Clone this repository:
```default
git clone https://github.com/georgiesamaha/configBuilder-nf.git
```

2. Install required packages: 
```default
pip install -r requirements.txt 
```

## Usage 

Execute `configBuilder-nf` by running the following from inside the configBuilder-nf directory: 

```default
python3 configBuilder
```

It is essential that you understand the infrastructure you are working on before you run this application. You will need to know the type of job scheduler used, the queue names and corresponding resource limits.  

### Prompts 

Follow the prompts carefully, ensuring you provide accurate details as per your HPC environment and pipeline requirements. The tool simplifies the configuration process, making it more intuitive and user-friendly for those deploying Nextflow or nf-core pipelines on HPC systems, however it cannot validate your inputs are correct.

You will be asked a series of questions regarding: 

* **Pipeline source:** You'll first be asked if you're generating this configuration file for an nf-core or a custom Nextflow pipeline. 
* **Pipeline selection:** If you select nf-core you'll be asked to name the nf-core pipeline you intend to apply the generated config file to. 
* **Executor selection:** You'll be prompted to select the [job scheduler](https://www.nextflow.io/docs/latest/executor.html#executors) (executor) that your HPC system uses. Choose one from the list, or specify local.
* **Module preloading:** Specify any modules and their versions that should be loaded before each process. Multiple modules can be separated by spaces. This employs the beforeScript operator to preload necessary modules for your HPC environment.
* **Compute resources:** If you've not selected local as the executor, you'll be prompted to:
    * Specify the **queue** in which to run your jobs.
    * Provide any additional **cluster options**. 
    * Define the maximum number of **CPUs, memory in GB, and walltime in hours** for each process.
* **Label-specific resources:** The application allows you to specify unique resource needs for [specific labels](https://www.nextflow.io/docs/latest/config.html?highlight=withname#process-selectors). This can be especially useful when certain stages or steps in your pipeline have different computational requirements.
* **Process-specific resources:** You can define resources for specific processes based on their [name](https://www.nextflow.io/docs/latest/config.html?highlight=withname#process-selectors), further tailoring your configuration to match the requirements of individual steps in your pipeline.
* **Post-run clean up:** You have the option to enable [cleanup](https://www.nextflow.io/docs/latest/config.html?highlight=cleanup#miscellaneous) after your runs, ensuring that temporary files and data are removed to free up space.

Once all prompts have been answered, the application will generate the custom config. 

### Apply your custom config

Run your pipeline using your custom config file by using the `-c <your-config>.config` flag. For example, to test the nf-core/rnaseq pipeline with a custom configutation generated with this tool, run: 

```default
nextflow run nf-core/rnaseq/main.nf \
    -profile test,singularity \
    -c custom_nfcore.config \
    --outdir <OUTDIR>
```

## Considerations

Keep the following limitations in mind when using this application: 

* This tool was developed using features provided by Nextflow v23.04.1
* It is only designed to work with Nextflow supported executors 
* The tool assumes the use of a module system for software management (beforeScript operator). If the HPC environment doesn't use module loading or uses a different system, this feature might not be beneficial
* This tool provides no error handling or validation of the generated config 
* While the tool allows users to specify resources like CPU, memory, and walltime, it doesn't provide guidance or estimates on what is appropriate for the infrastructure
* This tool is limited to Nextflow-supported job schedulers only. 

## Acknowledgements 

This application was developed as a part of the [nf-core mentorship program](https://nf-co.re/mentorships) with the support of the [Sydney Informatics Hub](https://github.com/Sydney-Informatics-Hub), a Core Research Facility of the University of Sydney and the Australian BioCommons which is enabled by NCRIS via Bioplatforms Australia. 

### Contributors

* Georgie Samaha (@georgiesamaha)
* Cristina Tuñí i Domínguez (@ctuni)
* Cali Willet (@calliza)