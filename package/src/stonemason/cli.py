"""Stonemason

A tool for working with composable project templates. 

Usage:
    mason init [-o DIR] [PROJECT]
    mason add [-o DIR] [TEMPLATE ...]
    mason (-h | --help)
    mason --version

Arguments:
  PROJECT      URL/Filepath to directory for project type. Should contain
               subdiectories for all templates. Can specify a project and
               one or more templates after the directoty as in 
               PROJECT:TEMPLATE[:TEMPLATE ...]
  TEMPLATE     Name of template directry to use from PROJECT dir

Options:
  -o DIR --output=DIR  Project directory to create/add to [default: .]
  -h --help            Show this screen.
  --version            Show version.
"""
import os
from sys import exit

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
        mason_path = os.path.join(output, '.mason.json')
        return os.path.exists(mason_path)
    
    if args['init']:
        schema = Schema({
            # 'TEMPLATE': And(template_path_exists, error='TEMPLATE should be subdirectory of PROJECT'),
            # 'PROJECT': And(os.path.exists, error='PROJECT should exist'),
            str: object})

    elif args['add']:
        schema = Schema({
            # 'TEMPLATE': And(str, error='TEMPLATE should be specified'),
            # '--output': And(mason_file_exists, error='The .mason.json was not detected for project.'
            #                                          ' Specofy location with --output option.'),
            str: object})
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)


def parse_and_validate_args():
    args = parse_args()
    validate_args(args)
    return args
