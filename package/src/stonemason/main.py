"""Main Entry point to stonemason"""

import pathlib

from .cli import parse_and_validate_args
from .initialise_project import initialise_project


def main():

    # Read in Arguments
    args = parse_and_validate_args()
    print(args)

    if args['init']:

        # Split project argument to project and template if needed
        if ':' in args['PROJECT'] and not args['TEMPLATE']:
            project_dir, template = args['PROJECT'].split(':')
        else:
            project_dir = args['PROJECT']
            template = args['TEMPLATE'] if args['TEMPLATE'] else None
            
        # intialise a new project based on template
        initialise_project(
            project=project_dir, 
            template=template, 
            output_dir=args['--output'])

    elif args['add']:

        # Find information about the current project
    
        # Add the right template
        add_template(args, )


if __name__ == '__main__':
    main()