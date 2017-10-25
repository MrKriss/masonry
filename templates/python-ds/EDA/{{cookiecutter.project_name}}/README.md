# {{ cookiecutter.project_name }}

> {{cookiecutter.short_description}}

### Authors

* {{ cookiecutter.author }}

## Quick Start

* Notebooks in the `analysis/` directory are numbered sequentially and represent individual steps and/or experiments. Stepping through them in order will recreate the steps. Supporting code is contained in python modules in the same directory. 

* Data and all associated metadata live in a subdirectory of `data/`.

* Outputs of analysis are in the `outputs/` directory.

Note that [python-dotenv](https://github.com/theskumar/python-dotenv) is used to load any secret keys and passwords from a `.env` file in the root directory of this project. If storing secret info is required, you will need to create this file. 
