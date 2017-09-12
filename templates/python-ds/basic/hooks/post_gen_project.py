""" Hooks to create a new conda environment with the latest version of common libraries 

"""

import subprocess
import shlex

# The string in these variables will be overriden by cookiecutter
PROJECT_NAME = "{{cookiecutter.project_name|lower|replace(' ', '_')}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"
PYTHON_LIBRARIES = "{{cookiecutter.python_libraries}}"
if PYTHON_LIBRARIES == "NONE":
    PYTHON_LIBRARIES = ""

# Create the strings for commands to run, substituting with the values from cookiecutter
conda_install_cmd_tpl = "conda create -y -n {project_name} python={python_version} {python_libraries}"
conda_install_cmd = conda_install_cmd_tpl.format(project_name=PROJECT_NAME,
                                                 python_version=PYTHON_VERSION,
                                                 python_libraries=PYTHON_LIBRARIES)
conda_save_env_cmd = "conda env export -n {project_name} -f frozen_environment.yml".format(
    project_name=PROJECT_NAME)

# Execute command with subprocess module
print('\nInstalling conda environment for %s ...\n' % PROJECT_NAME)
subprocess.run(shlex.split(conda_install_cmd))
print('\nFinished installing conda environment for %s \n' % PROJECT_NAME)

print('\nSaving snapshot of conda environment to "frozen_environment.yml" ... \n')
subprocess.run(shlex.split(conda_save_env_cmd))
print('\nComplete!\n')
