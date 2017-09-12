""" Hooks to create a new conda environment with the latest version of common libraries 

Also optionally create a git repo and commit the project contents
"""

import subprocess
import shlex
import pathlib
import shutil
from stonemason.utils import prefix, postfix

import os

print(os.getcwd())


postfix('package/MANIFEST.in', 'package/MANIFEST_postfix.in')
postfix('package/requirements.txt', 'package/requirements_postfix.txt')
postfix('Makefile', 'Makefile_postfix')


print('Commiting changes ...')
subprocess.run(shlex.split('git add ./package/'))
subprocess.run(shlex.split('git commit -m "Add package tests layer"'))
print("Complete!!!")
