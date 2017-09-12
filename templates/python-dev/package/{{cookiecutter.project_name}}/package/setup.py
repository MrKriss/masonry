# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='{{cookiecutter.package_name}}',
    description='{{cookiecutter.short_description}}',
    author='Chris Musselle',
    author_email='chris.j.musselle@gmail.com',
    # Required for packaging source distribution from 'src' subfolder
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    { % if cookiecutter.entry_point % }
    # This next section registers 'mycommand' as a command line utility that will execute
    # the `command_line_entry_point()` function in the `command_line` module of `mypackage`
    entry_points={
        'console_scripts': [
            'rss-miner=rss_miner.main:cli_entry_point'
        ]
    },
    { % endif % }
    # include_package_data=True,
    package_data={'rss_miner': ['example_config.yml']},
    # Use version control to define version tag
    use_scm_version={"root": "..", "relative_to": __file__}
)
