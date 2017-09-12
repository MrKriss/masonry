""" Post project creation hooks: 

Ask whether to transfer .py files under analysis/ to package src.

Move dev/frozen environment files to package directory

"""

{% if cookiecutter.transfer_analysis_scripts_to_package == "Yes" %}
import shlex
import pathlib
import shutil
import os

scripts_dir = pathlib.Path('.').absolute() / 'analysis'
n = 0
for file_ in scripts_dir.glob('*.py'):
    shutil.move(file_.as_posix(), './package/src/{{cookiecutter.package_name}}')
    n += 1
print('Moved %d .py files to package/src/{{cookiecutter.package_name}}' % n)
{% endif %}

# Move environment files
environment_files = pathlib.Path('.').absolute().glob('*environment.yml')
for file_ in environment_files:
    shutil.move(file_.as_posix(), './package/')
