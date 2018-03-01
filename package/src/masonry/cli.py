"""Masonry

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

  TEMPLATE     Name of one or more templates to add to an existing project.

Options:
  -o DIR --output=DIR  Project directory to create/add to [default: .]
  -h --help            Show this screen.
  --version            Show version.
  -v                   Increase verbosity of output
"""
from pathlib import Path
from sys import exit

from docopt import docopt
from schema import Optional, Or, Schema, SchemaError, Use

from . import __version__


class CLI:

    def __init__(self, args, config=None):
        self.args = docopt(__doc__, version=__version__, argv=args)
        self.args = MasonrySchema(self.args).validate()

    def _validate_args(self):
        args = MasonrySchema(self.args).validate()
        return args


class MasonrySchema:

    def __init__(self, args):

        def check_path(path):
            if path is not None:
                path = Path(path).expanduser().resolve(strict=True)
            return path

        def check_mason_file_present(path):
            path = check_path(path)
            mason_path = path / '.mason'
            mason_path.resolve(strict=True)
            return path

        if args['init']:
            schema = Schema({
                Optional('PROJECT'): Use(
                    check_path,
                    error='Supplied PROJECT path does not exist.'
                ),
                Optional('--output'): Use(
                    check_path,
                    error='Supplied output path does not exist.'
                ),
                str: object
            })
        elif args['add']:
            schema = Schema({
                Optional('TEMPLATE'): Or(str, list),
                Optional('--output'): Use(
                    check_mason_file_present,
                    error='The .mason file was not detected for project. '
                          'Specify location with --output option.'
                ),
                str: object}
            )
        elif args['check']:
            schema = Schema({
                Optional('PROJECT'): Use(
                    check_path,
                    error='Supplied PROJECT path does not exist.'
                ),
                str: object}
            )

        self.schema = schema
        self.args = args

    def validate(self):

        try:
            args = self.schema.validate(self.args)
        except SchemaError as e:
            exit(e)

        return args
