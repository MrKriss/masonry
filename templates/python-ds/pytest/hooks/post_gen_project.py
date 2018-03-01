""" Post project creation hooks:

Install new libraries according to dev_environment.yml

"""

from pathlib import Path
import shutil

from masonry.hook_utils import run_and_capture
from clint.textui import indent, colored, puts


PROJECT_NAME = "{{cookiecutter.project_name|lower|replace(' ', '_')}}"

conda_update_cmd = f"conda env update -n {PROJECT_NAME} -f package/dev_environment.yml"

with indent(4):
    puts("Updating dependencies from new dev_environment.yml")
    p = run_and_capture(conda_update_cmd)
