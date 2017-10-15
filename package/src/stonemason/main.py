"""Main Entry point to stonemason"""

from .cli import parse_and_validate_args, parse_project_argument
from .template import initialise_project, add_template
from .utils import load_application_data
from .prompt import prompt_init_project, prompt_add_template

import os
import json
from pathlib import Path

from .utils import setup_logger


def main(args=None):

    # Read in Arguments
    args = parse_and_validate_args(args)

    if args['-v']:
        logger = setup_logger(logfile=None, level='DEBUG')
    else:
        logger = setup_logger(logfile=None, level='INFO')

    logger.debug(f'Passed Arguments: {args}')

    project_templates = load_application_data()

    if args['init']:

        template = None

        # Get project
        if not args['PROJECT']:
            if project_templates:
                # Launch inquire
                project_dir = prompt_init_project(project_templates)
            else:
                raise ValueError("No known projects to choose from. "
                                 "Add one using the PROJECT argument.")
        else:
            project_dir, template = parse_project_argument(args['PROJECT'])

        # intialise a new project based on template
        output_dir = Path(args['--output']).resolve()

        initialise_project(
            project=project_dir,
            template=template,
            output_dir=output_dir)

    elif args['add']:

        project_dir = Path(args['--output']).resolve()

        # Load existing state information
        mason_vars = project_dir / '.mason'

        if not mason_vars.exists():
            raise IOError(f'A ".mason" file was not detected int he output directoty {project_dir}')

        with mason_vars.open('r') as f:
            project_state = json.load(f)

        project_templates_root = project_templates[project_state['project']]

        # Get project template options
        if not args['TEMPLATE']:
            # inquire which template to use
            args['TEMPLATE'] = prompt_add_template(project_templates_root, project_state)

        # Add the right template
        add_template(templates=args['TEMPLATE'],
                     project_dir=args['--output'])


if __name__ == '__main__':
    main()
