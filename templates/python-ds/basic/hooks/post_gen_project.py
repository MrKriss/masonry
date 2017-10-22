""" Hooks to create a new conda environment with the latest version of common libraries

"""

from clint.textui import indent, puts
from stonemason.utils import run_and_capture

# The string in these variables will be overriden by cookiecutter
PROJECT_NAME = "{{cookiecutter.project_name|lower|replace(' ', '_')}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"
PYTHON_LIBRARIES = "{{cookiecutter.python_libraries}}"
if PYTHON_LIBRARIES == "NONE":
    PYTHON_LIBRARIES = ""

# Create the strings for commands to run, substituting with the values from cookiecutter
conda_install_cmd = ("conda env create -f dev_environment.yml")
conda_save_env_cmd = f"conda env export -n {PROJECT_NAME} -f frozen_environment.yml"

# Use clint library to frmat console output
with indent(4):
    puts("Create new conda environment...")
    p = run_and_capture(conda_install_cmd)
    puts("Snapshot conda environment...")
    p = run_and_capture(conda_save_env_cmd)
