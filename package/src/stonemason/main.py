"""Main Entry point to stonemason"""

import json
import os
from pathlib import Path

from .cli import parse_and_validate_args, parse_project_argument
from .prompt import prompt_add_template, prompt_init_project
from .template import add_template, initialise_project
from .utils import load_application_data, setup_logger

from.check import check_templates


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
            raise IOError(f'A ".mason" file was not detected in the output directoty {project_dir}')

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

    elif args['check']:

        template = None

        # Find project to test
        if not args['PROJECT']:
            if project_templates:
                # Launch inquire
                template_collection_path = prompt_init_project(project_templates)
            else:
                raise ValueError("No known projects to choose from. "
                                 "Add one using the PROJECT argument.")
        else:
            project_dir, template = parse_project_argument(args['PROJECT'])

        # Check all template layers
        # Add the right template
        check_templates(template_collection_path=template_collection_path,
                        template=template)


if __name__ == '__main__':
    main()
