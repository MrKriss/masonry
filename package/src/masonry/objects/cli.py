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
import os
from sys import exit
from pathlib import Path

from docopt import docopt
import inquirer

from .. import __version__

from schema import Schema, And, Or, Use, Optional, SchemaError

from .project import Project


class CLI:

    def __init__(self, args, config=None):
        self.args = docopt(__doc__, version=__version__, argv=args)
        self.args = MasonrySchema(self.args).validate()

        if not config:
            self.config = {
                "application_data": "~/.masonry/",
                "known_projects": {}
            }
        else:
            self.config = config

    def _validate_args(self):
        args = MasonrySchema(self.args).validate()
        return args

    def run(self):

        self.args = self._validate_args()

        if self.args['init']:
            self.init_command()

        elif self.args['add']:
            self.add_command()

    def init_command(self, default_project=None):

        if not self.args['PROJECT']:
            self.args['PROJECT'] = self._prompt_init_project(default_project)

        project = Project(template_dir=self.args['PROJECT'])
        project.initialise(output_dir=self.args['--output'], variables={})
        self.project = project

    def add_command(self, default_template=None):

        project_dir = Path(self.args['--output']).resolve()
        mason_file = project_dir / '.mason'

        if not mason_file.exists():
            raise IOError(
                f'A ".mason" file was not detected in the output directoty {project_dir}')

        project = Project(mason_file=mason_file)

        if not self.args['TEMPLATE']:
            # inquire which template to use
            self.args['TEMPLATE'] = self._prompt_add_template(project, default_template)

        for template_name in self.args['TEMPLATE']:
            project.add_template(template_name, variables={})

        self.project = project

    def _prompt_init_project(self, default=None):
        """Return the choice of project to intialise"""

        known_projects = list(self.config['known_projects'].keys())
        known_projects.sort()

        if not known_projects:
            raise ValueError("No project specified and no recent projects to choose from.")

        if default:
            default_idx = known_projects.index(default)
        else:
            default_idx = 0

        questions = [
            inquirer.List('project',
                          message="What project do you want to initialise?",
                          choices=known_projects,
                          default=default_idx)
        ]
        answers = inquirer.prompt(questions)

        project_path = known_projects[answers['project']]

        return project_path

    def _prompt_add_template(self, project, default=None):
        """Return the choice of templates to add"""

        remaining_templates_names = project.remaining_templates

        if default:
            default_idx = known_projects.index(default)
        else:
            default_idx = 0

        questions = [
            inquirer.Checkbox('templates',
                              message="What templates do you wish to add?",
                              choices=remaining_templates_names,
                              default=default_idx)
        ]

        answers = inquirer.prompt(questions)

        templates = answers['templates']

        return templates


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
                    error='The .mason file was not detected for project. Specify location with --output option.'
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
