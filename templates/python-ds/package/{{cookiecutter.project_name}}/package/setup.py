# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='{{cookiecutter.package_name}}',
    description='{{cookiecutter.short_description}}',
    author='{{cookiecutter.author}}',
    author_email='{{cookiecutter.author_email}}',
    # Required for packaging source distribution from 'src' subfolder
    packages=find_packages(where='src', exclude='tests'),
    package_dir={'': 'src'},
    include_package_data=True,
    # Use version control to define version tag
    use_scm_version={"root": "..", "relative_to": __file__},
    # Unfrozen Dependencies
    install_requires=[
        {%- set python_libs = cookiecutter.python_libraries.split(' ') %}
        {%- if python_libs != ["NONE"] %}
        {%- for lib in python_libs %}
        '{{lib}}',
        {%- endfor %}
        {%- endif %}
    ],
    # This next section registers a command line utility that will execute
    # the `main()` function in the `main` module of `{{cookiecutter.package_name}}`
    # entry_points={
    #    'console_scripts': [
    #        '{{cookiecutter.package_name}}={{cookiecutter.package_name}}.main:main'
    #    ]
    # },
)
