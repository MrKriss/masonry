"""Stonemason

A tool for working with composable project templates. 

Commands:
    init  - initialise a new project 
    add   - add a template to an existing project
    check - check a particular project or template layer renders correctly

Usage:
    mason init [-v] [-o DIR] [PROJECT]
    mason add [-v] [-o DIR] [TEMPLATE ...]
    mason check [-v] [PROJECT]
    mason (-h | --help)
    mason --version

Arguments:
  PROJECT      URL/Filepath to directory for project type. Should contain
               subdiectories for all templates and a metadata.json file.
               Can also specify a template subdirectory, and if so, this
               is used as the template instead of the default for the project.

  TEMPLATE     Name of one or more templates to add to an existing project.

Options:
  -o DIR --output=DIR  Project directory to create/add to [default: .]
  -h --help            Show this screen.
  --version            Show version.
  -v                   Increase verbosity of output
"""
import os
from sys import exit
from pathlib import Path

from docopt import docopt

from . import __version__

try:
    from schema import Schema, And, Or, Use, SchemaError
except ImportError:
    exit('This example requires that `schema` data-validation library'
         ' is installed: \n    pip install schema\n'
         'https://github.com/halst/schema')


def parse_args(argv=None):
    args = docopt(__doc__, version=__version__, argv=argv)
    return args


def validate_args(args):
    def template_path_exists(template):
        if template:
            template_path = os.path.join(args['PROJECT'], template)
            return os.path.exists(template_path)
        else:
            return True

    def mason_file_exists(output):
        mason_path = os.path.join(output, '.mason')
        return os.path.exists(mason_path)

    if args['init']:
        schema = Schema({
            # 'TEMPLATE': And(template_path_exists, error='TEMPLATE should be subdirectory of PROJECT'),
            # 'PROJECT': And(os.path.exists, error='PROJECT should exist'),
            str: object})

    elif args['add']:
        schema = Schema({
            # 'TEMPLATE': And(str, error='TEMPLATE should be specified'),
            # '--output': And(mason_file_exists, error='The .mason was not detected for project.'
            #                                          ' Specofy location with --output option.'),
            str: object})

    elif args['check']:
        schema = Schema({
            # 'TEMPLATE': And(str, error='TEMPLATE should be specified'),
            # '--output': And(mason_file_exists, error='The .mason was not detected for project.'
            #                                          ' Specofy location with --output option.'),
            str: object})
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)


def parse_and_validate_args(argv):
    parsed_args = parse_args(argv)
    validate_args(parsed_args)
    return parsed_args


def parse_project_argument(arg):

    template = None

    # See if template directroy or project directory was specified
    project_argument = Path(arg).resolve()
    project_metadata = project_argument / 'metadata.json'

    if project_metadata.exists():
        project_dir = arg

    elif (project_argument.parent / 'metadata.json').exists():
        # Check parent directory and use sub directory as template
        project_dir = project_argument.parent.as_posix()
        template = project_argument.name

    return project_dir, template
