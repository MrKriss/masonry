""" Post project creation hooks: 

Ask whether to transfer .py files under analysis/ to package src.

Move dev/frozen environment files to package directory

"""

from pathlib import Path
import shutil

from clint.textui import indent, colored, puts

TRANSFER_SCRIPTS = "{{cookiecutter.transfer_analysis_scripts_to_package}}" == 'Yes'

with indent(4):
    if TRANSFER_SCRIPTS:
        scripts_dir = Path('.').absolute() / 'analysis'
        n = 0
        for file_ in scripts_dir.glob('*.py'):
            shutil.move(file_.as_posix(), './package/src/{{cookiecutter.package_name}}')
            n += 1
        puts('Moved %d .py files to package/src/{{cookiecutter.package_name}}' % n)

    puts('Move environment files to package/')
    environment_files = Path('.').absolute().glob('*environment.yml')

    for file_ in environment_files:
        shutil.move(file_.as_posix(), './package/')
