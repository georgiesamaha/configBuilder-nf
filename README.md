# configBuilder-nf: create custom Nextflow configs

<p align="center">
:wrench: This tool is currently under development :wrench:
</p>

**Developers please see [development guide](DEVELOPMENT.md) for resources and how to contribute**

configBuilder-nf is a Python-based application for building custom configuration files for running your Nextflow and nf-core pipelines for High Performance Computing (HPC) infrastructures. This tool uses command-line prompts to collect specific details from you regarding the HPC job scheduler your system works with, compute resources available to you, and more. The collected inputs are then formatted and written to a configuration file, making it easier for uses to deploy pipelines on HPC infrastructures.

## Installation 

To run this application you will need to have Python3 installed and the following Python packages: 

* [colorama](https://pypi.org/project/colorama/)
* [inquirer](https://pypi.org/project/inquirer/)

1. Clone this repository:
```default
git clone https://github.com/georgiesamaha/configBuilder-nf.git
```

2. Change into the repository and install required packages

   a. With pip

   ```default
   pip install -r requirements.txt 
   ```

   b. With conda

   ```default
   conda env -f environment.yml
   conda activate configbuilder-nf
   ```
   
## Usage 

Execute `configBuilder-nf` by running the following from inside the configBuilder-nf directory: 

```default
python3 configBuilder
```

It is essential that you understand the infrastructure you are working on before you run this application. You will need to know the type of job scheduler used, the queue names and corresponding resource limits.  

### Prompts 

Follow the prompts carefully, ensuring you provide accurate details as per your HPC environment and pipeline requirements. The tool simplifies the configuration process, making it more intuitive and user-friendly for those deploying Nextflow or nf-core pipelines on HPC systems, however it cannot validate your inputs are correct. 

Prompts are currently WIP, it currently tests for: 

* **Pipeline source:** You'll first be asked if you're generating this configuration file for an nf-core or a custom Nextflow pipeline. 
* **Your execution environment:** Are you running your workflow on HPC, cloud, or local machine (currently only HPC functional). 
* **Availability of a Singularity module:** Can singularity be enabled on your system to run containers. 
* **Your config name:** What do you want your custom config to be called (default: custom_nextflow.config)

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

* This tool is a WIP 
* This tool was developed using features provided by Nextflow v23.04.1
* It is only designed to work with Nextflow supported executors 
* The tool assumes the use of a module system for software management (beforeScript operator). If the HPC environment doesn't use module loading or uses a different system, this feature might not be beneficial
* This tool provides no error handling or validation of the generated config 
* While the tool allows users to specify resources like CPU, memory, and walltime, it doesn't provide guidance or estimates on what is appropriate for the infrastructure

## Acknowledgements 

This application was developed as a part of the [nf-core mentorship program](https://nf-co.re/mentorships) with the support of the [Sydney Informatics Hub](https://github.com/Sydney-Informatics-Hub), a Core Research Facility of the University of Sydney and the Australian BioCommons which is enabled by NCRIS via Bioplatforms Australia. 

### Contributors

* Georgie Samaha (@georgiesamaha)
* Cristina Tuñí i Domínguez (@ctuni)
* James A. Fellows Yates (@jfy133)
* Cali Willet (@calliza)
