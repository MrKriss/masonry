# Masonry

[![build status](http://img.shields.io/travis/MrKriss/masonry/master.svg?style=flat)](https://travis-ci.org/MrKriss/masonry) 
[![codecov](https://codecov.io/gh/MrKriss/masonry/branch/master/graph/badge.svg)](https://codecov.io/gh/MrKriss/masonry)

> A command line tool for composable project templating. 

Masonry aims to reduce the need to write boiler plate code and setup files when starting or 
extending a project. It does so by allowing [cookiecutter](https://github.com/audreyr/cookiecutter) 
templates to be combined in a series of layers to build up a projects file structure.  

Applying different combinations of these template building blocks then allow for a greater variety of 
project types to be more easily supported, compared to defining each template permutation separately. 

Masonry also includes a cli application `mason` that makes applying and managing these template 
layers straight forward.  

# Installation 

    pip install masonry

## Key Dependencies:

* `cookiecutter` >= 1.6

# Usage 

1. Create a series of template layers to use for a particular project layout (see below and in the 
project-templates directory for examples).

2.  Initialise a new project with its default starting template

        mason init project/template/path

3.  Add an extra templating layer to the project

        mason add template_name


# Creating and Using Template Layers for a Custom Project

The individual template layers are themselves cookiecutter templates. To combine several of these 
into a project to use with masonry:

* Each cookiecutter template should be in its own directory named after the templates purpose
* All these are then held in a parent directory, which is named after the project type all these 
layers relate to.
* Included in the project group directory is a metadata.json file that specifies the "default" 
  template to use, as well as any dependencies between layers.

For example, imagine a situation that wished to combine the following three layers into a project:

1. One to create a base python package
2. Another to define the unittest structure with pytest
3. A third to add a build file for continuous integration.

Placing these all in the same directory called "python-project" would give the following structure:

```
path/to/python-project/
            ├── ci-build
            │   ├── {{cookiecutter.project_name}}
            │   └── cookiecutter.json
            │ 
            ├── package
            │   ├── {{cookiecutter.project_name}}
            │   └── cookiecutter.json
            │  
            ├── pytest
            │   ├── {{cookiecutter.project_name}}
            │   └── cookiecutter.json
            │
            └── metadata.json
```

The metadata.json file would then specify the *package* template as the default layer, with the 
*pytest* template layer depending on the *package* template, and the *ci-build* template layer 
depending on the *pytest* template. The structure of the resulting JSON file is shown below: 

```json
{
    "default": "package", 
    "dependencies": {
        "pytest": ["package"], 
        "ci-build": ["pytest"]
    }
}
```

Now using `mason` we can create a new project following the *package* template with:

```bash
    mason init path/to/python-project/
```

And at a later time, when we want to start adding tests and a build process to the project, we 
could run: 

```bash
    mason add ci-build
```

Note that even though we only specified "ci-build" above, `mason` is able to work out all needed 
template layer dependencies from the metadata.json and apply them in the right order. This means
both the *pytest* and *ci-build* template layers will be applied in that order. 


# Projects as a Collection of Components

Splitting out the templates above may not seem to have gained you very much. After all, you 
could have just defined all these files for package + tests + CI in a single template structure. 
However, as you start to add different components to your projects under different scenarios, this 
modular approach becomes more beneficial.

For example, say you wanted to support different CI services such as circle CI, travis, and GitLab Runners
on different projects; and on some projects you have a Makefile, and on others something more cross 
platform compatible like an invoke tasks.py file. 

Accommodating all these options would either mean maintaining 6 different templates with a lot of 
repetition, or one large one with a lot of control flow logic in the jinja template. 

Stomemason provides a middle ground of breaking up these components of the project into separate layers. 

It also has the major benefit of being able to apply any additional layers **after** the initial 
project was created. So if you didn't see the need to also create a conda package for your project 
till now? No problem, just apply the conda-package layer to the current project (assuming you have 
defined one of course!).

# Additional Features

* Pre and post project creation hooks used by cookiecutter are supported.
* Cookiecutter variables are remembered and reused between template layers, meaning you only need 
to specify values for new variables. 
* If project path is omitted, `mason init` allows you to interactively select one from a list of previously
  used projects. 
* If the template name is omitted, `mason add`, allows you to interactively select one from a list 
of templates that can still be added to the project.  
* Colourful UI and easy multiple choice selection thanks to the [inquirer](https://github.com/magmax/python-inquirer)
library.
  

# Other Related Projects

* [python boilerplate](https://www.python-boilerplate.com) A web application for interactively filling 
out a template for a new project. 

* [yeoman](http://yeoman.io/) A project scaffolding tool for web development written in javascript. 

* [mason](https://github.com/metacran/mason) A project in R similar to cookiecutter but with a 
colourful UI, and one of the inspirations for this project. 

* [usethis](https://github.com/r-lib/usethis) A project in the R community looking at similar ideas 
around project template composability, and being able to add them as needed on a project. 

