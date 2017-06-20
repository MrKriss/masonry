""" Hooks to create a new conda environment with the latest version of common libraries 

Also optionally create a git repo and commit the project contents
"""

import subprocess
import shlex
import pathlib
import shutil

import os

print(os.getcwd())

# Ask if wanting to transfer script .py files to package?
{% if cookiecutter.transfer_scripts_to_package == "Yes" %}

scripts_dir = pathlib.Path('.').absolute() / 'scripts'
n = 0
for file_ in scripts_dir.glob('*.py'):
    if not os.path.exists('./package/src/{{cookiecutter.package_name}}'):
        shutil.move(file_.as_posix(), './package/src/{{cookiecutter.package_name}}')
    n += 1
print('Moved %d .py files to package/src/{{cookiecutter.package_name}}' % n)

with open('Makefile', 'a') as fout:
    with open('Makefile_postfix') as fin:
        fout.write(fin.read())
print('Appended test build target to Makefile')
os.remove(fin.name)

print('Commiting changes ...')
subprocess.run(shlex.split('git add ./scripts/'))
subprocess.run(shlex.split('git add ./package/'))
subprocess.run(shlex.split('git commit -m "Add package template layer"'))
print("Complete!!!")
{% endif %}

# TODO
# Add generation of requiremetns.txt from libraries list saved on environment creation?

# Use defult libs list 