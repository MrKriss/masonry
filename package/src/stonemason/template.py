
from pathlib import Path
import json
import sys

from .resolution import create_dependency_graph, resolve
from .render import render_cookiecutter
from .utils import load_application_data, save_application_data

from.prompt import prompt_cookiecutter_variables


from clint.textui import prompt, puts, colored, validators


def initialise_project(project, template=None, output_dir='.'):

    # Initialise path variables
    project_path = Path(project).resolve()
    meta_data_path = project_path / 'metadata.json'
    project_templates = load_application_data()

    # If project is a valid project file 
    if not meta_data_path.exists():
        raise IOError("Not a valid project directory. Missing matadata.json file")

    if not template:
        # Load metadata for project and read in default template from there
        with meta_data_path.open() as meta_data_file:
            meta_data = json.load(meta_data_file)
        template = meta_data['default']

    # Store location of project template
    if project_path.name in project_templates:
        if project_templates[project_path.name] != project_path.as_posix():
            ans = prompt.query(
                "Project with the same name already exists in another location. Overwrite? [y/n]", 
                validators=[validators.RegexValidator('[yn]')])
            if ans == 'n':
                sys.exit()

    project_templates[project_path.name] = project_path.as_posix()
    save_application_data(project_templates)

    # Work out all template names
    template_paths = {p.name: p for p in project_path.iterdir() if p.is_dir()}
    template_names = list(template_paths.keys())

    # Create graph of template dependencies
    g = create_dependency_graph(project_path / 'metadata.json',
                                node_list=template_names)

    # Resolve dependencies for specified template
    template_order = [n.name for n in resolve(g[template])]
    puts(f'Creating project from templates:\n\t{template_order}')

    # Initialise output structure to save state of project
    project_state = {}
    project_state['templates'] = []
    project_state['variables'] = {}

    # Cycle through templates and render them
    for name in template_order:
        template = template_paths[name].as_posix()
        context_variables = prompt_cookiecutter_variables(template, project_state['variables'])

        project_dir, content = render_cookiecutter(
            template, no_input=True,
            extra_context=context_variables,
            output_dir=output_dir, overwrite_if_exists=True,
        )

        puts(f'Rendered: {template}')

        # Save state
        project_state['variables'].update(content)
        project_state['templates'].append(name)
        project_state['project'] = project_path.name

    # Save state of project variables
    mason_vars = Path(project_dir) / '.mason.json'
    with mason_vars.open('w') as f:
        json.dump(project_state, f)


def add_template(templates, project_dir, output_dir='.'):
    """ Add a template to an existing project """

    project_dir = Path(project_dir).resolve()

    # Load existing state information
    mason_vars = project_dir / '.mason.json'
    with mason_vars.open('r') as f:
        project_state = json.load(f)

    # Load project locations and get project root path
    project_template_data = load_application_data()
    project_root = Path(project_template_data[project_state['project']])

    # Find remaining templates that can be applied
    previous_templates = project_state['templates']  
    paths = project_root.iterdir()
    remaining_template_paths = {
        p.name: p for p in paths if p.is_dir() and p.name not in previous_templates
    }
    remaining_templates_names = list(remaining_template_paths.keys())
    remaining_templates_names.sort()

    for t in templates:
        assert t in remaining_template_paths, f'{t} not in remaining templates'

    # Create graph of template dependencies
    g = create_dependency_graph(project_root / 'metadata.json',
                                node_list=remaining_templates_names)

    # Resolve dependencies for specified template
    template_orders = []
    
    for t in templates:
        order = [n.name for n in resolve(g[t]) if n.name not in previous_templates]
        template_orders.append(order)
        previous_templates.extend(order)

    puts(f'Adding the following templates to project:\n\t{template_orders}')

    # Cycle through templates and render them
    for order_set in template_orders:

        for name in order_set:
            template = remaining_template_paths[name].as_posix()
            context_variables = prompt_cookiecutter_variables(template, project_state['variables'])
            project_state['variables'].update(context_variables)

            output_project_dir, content = render_cookiecutter(
                template, no_input=True,
                extra_context=project_state['variables'],
                output_dir=project_dir.parent, overwrite_if_exists=True,
            )
            puts(f'Rendered: {template}')

            # Save state
            project_state['variables'].update(content)
            project_state['templates'].append(name)

    # Save state of project variables
    with mason_vars.open('w') as f:
        json.dump(project_state, f)
