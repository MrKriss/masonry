# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='{{cookiecutter.package_name}}',
    description='{{cookiecutter.short_description}}',
    author='{{cookiecutter.author}}',
    author_email='{{cookiecutter.email}}',
    # Required for packaging source distribution from 'src' subfolder
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    # This next section registers 'mycommand' as a command line utility that will execute
    # the `cli_entry_point()` function in the `command_line` module of `mypackage`
    #entry_points={
    #    'console_scripts': [
    #        'mycommand=mypackage.main:cli_entry_point'
    #    ]
    #}
)
