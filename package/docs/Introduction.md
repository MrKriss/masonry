Motivation
----------

Project templating and scaffolding tools like [cookiecutter](https://github.com/audreyr/cookiecutter) 
can be a great help when starting a new project. They provide a way of generating a predefined layout of files and directories for a new project, and can also be parameterised to accept arguments as they are generated. e.g. name of the new project.

Creating such a template takes some effort but means quicker startup times on future projects; less boiler plate code to write; more consistent project layouts; and even automation of common setup tasks.

However, I often find the projects I work on are quite varied in their needs, and it can be difficult to have a single template or series of templates that can cover all types of project. Often I've found myself with one monolithic template that tries to do everything, and then have to spend time deleting or tweaking parts that aren't relevant to the new project I just created. And if I have too many templates for different needs, then maintaining them and remembering which is which increasingly becomes a burden as the list grows. 

Stonemason takes a slightly different approach to project templating, whilst at the same time building on the capabilities already present in cookiecutter. Instead of files and folders being generated once at project creation for a given template,
the project template is composed of one or more "layers" that can be applied as and when needed. Each layer can specify  dependencies on previous layers, and reuse the cookicutter variables already declared.  

The goal of stonemason is to cater for more project variety when templating, by allowing for the composability of smaller template components (layers). Stonemason then also provides a helpful cli tool to apply these throughout the lifetime of a project. 

