""" Hooks to create a new conda environment with the latest version of common libraries 

Also optionally create a git repo and commit the project contents
"""

from stonemason.utils import postfix

postfix('requirements.txt', 'requirements_postfix.txt')

