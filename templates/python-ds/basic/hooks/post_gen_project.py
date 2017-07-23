""" Hooks to create a new conda environment with the latest version of common libraries 

Also optionally create a git repo and commit the project contents
"""

import subprocess
import shlex

# The string in these variables will be overriden by cookiecutter
PROJECT_NAME = "{{cookiecutter.project_name|lower|replace(' ', '_')}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"
PYTHON_LIBRARIES = "{{cookiecutter.python_libraries}}"

# Create the strings for commands to run, substituting with the values from cookiecutter 
conda_install_cmd_tpl = "conda create -y -n {project_name} python={python_version} {python_libraries}"
conda_install_cmd = conda_install_cmd_tpl.format(project_name=PROJECT_NAME,
                                                 python_version=PYTHON_VERSION,
                                                 python_libraries=PYTHON_LIBRARIES)
conda_save_env_cmd = "conda env export -n {project_name} -f environment.yml".format(project_name=PROJECT_NAME)

# Execute command with subprocess module
print('Installing conda environment for %s ...' % PROJECT_NAME)
subprocess.run(shlex.split(conda_install_cmd))
print('Finished installing conda environment for %s ' % PROJECT_NAME)

print('Saving snapshot of conda environment to "environment.yml" ... ', end='')
subprocess.run(shlex.split(conda_save_env_cmd))
print('Complete!')


# If using git, initialise the rep.
# The code in this following Jinja2 block only gets inserted when "git_usage" is set to Yes
{% if cookiecutter.git_usage == "Yes" %}
print('Initialising Git repo and creating initial commit for %s ...' % PROJECT_NAME)
subprocess.run(shlex.split('git init'))
subprocess.run(shlex.split('git add *'))
subprocess.run(shlex.split('git commit -m "Initial commit of basic project template layer"'))
print("Complete!!!")
{% endif %}
