# configBuilder-nf

Assisted custom Nextflow config file builder for pipelines written in DSL2 and nf-core pipelines. 

Currently 2 modules under development: 
1. Nextflow pipeline config builder 
2. nf-core pipeline config builder

Download code base: 
```default
git clone https://github.com/georgiesamaha/configBuilder-nf.git
```

Install required Python packages: 
```default
pip install -r requirements.txt 
```

Execute with:
```default
python3 configBuilder
```

## Nextflow config builder 

* Simple HPC config builder that submits tasks as jobs to scheduler or local tasks
* Preloads modules with `beforeScript` operator 
* Set max walltime, cpu, memory for queue
* Set process-specific scope as needed 
* Enables Singularity 
* Outputs custom_nextflow.config

## nf-core config builder 

* Simple HPC config builder that submits tasks as jobs to scheduler or local tasks
* Preloads modules with `beforeScript` operator 
* Set max_time, max_cpu, max_memory for workflow
* Set process-specific scope and resources as needed 
* Set label-specific scope and queue as needed 
* Outputs custom_nfcore.config
