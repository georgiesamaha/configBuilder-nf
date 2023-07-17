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
* TODO: Ask if want to trace resource usage for efficiency evaluation
* TODO: Set number of retries with increasing resources 
* TODO: Set max walltimes

## nf-core config builder 

* TODO: design configuration specifications 