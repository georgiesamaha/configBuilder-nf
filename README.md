# configBuilder-nf

Assisted custom Nextflow config file builder for pipelines written in DSL2 and nf-core pipelines. 

Currently 2 modules under development: 
1. Nextflow pipeline config builder 
2. nf-core pipeline config builder

Execute with:
```default
python3 configBuilder
```

## Nextflow config builder 

* Simple HPC config builder that submits tasks as jobs to scheduler or local tasks
* Preloads modules with `beforeScript` operator 
* Set max walltime, cpu, memory for queue
* Set process-specific scope as needed 
* Enable Singularity 
* TODO: Tower functionality option 
* TODO: Ask if want to trace resource usage for efficiency evaluation
* TODO: Set number of retries with increasing resources 

## nf-core config builder 

* Simple HPC config builder that submits tasks as jobs to scheduler or local tasks
* Preloads modules with `beforeScript` operator 
* Set max_time, max_cpu, max_memory for workflow
* Set process-specific scope as needed 
* TODO: assign queue based on flexible resource requrements
* TODO: explore if pipeline-specific features are required
* TODO: explore withLabel resource requirements 

## Workflow resource usage evaluation 

* TODO: scope functionality 