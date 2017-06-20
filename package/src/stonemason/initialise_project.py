
from pathlib import Path
import json

from .resolution import create_dependency_graph, resolve
from .render import render_cookiecutter


def initialise_project(project, template=None, output_dir='.'):

    project_path = Path(project)

    if not template:
        # Load metadata for project and read in default template from there
        meta_data_path = project_path / 'metadata.json'
        with meta_data_path.open() as meta_data_file:
            meta_data = json.load(meta_data_file)
        template = meta_data['default']

    # Work out all template names
    template_paths = {p.name: p for p in project_path.iterdir() if p.is_dir()}
    template_names = list(template_paths.keys())

    # Create graph of template dependencies
    g = create_dependency_graph(project_path / 'metadata.json',
                                node_list=template_names)

    # Resolve dependencies for specified template
    template_order = [n.name for n in resolve(g['package'])]
    print(f'Creating project from templates:\n\t{template_order}')

    # Cycle through templates and render them
    content_variables = {}
    for name in template_order:
        template = template_paths[name].as_posix()
        project_dir, content = render_cookiecutter(
            template,
            extra_context=content_variables,
            output_dir=output_dir, overwrite_if_exists=True,
        )
        print(f'Rendered: {template}')
        content_variables.update(content)

    # Save state of project variables
    mason_vars = Path(project_dir) / '.mason.json'
    with mason_vars.open('w') as f:
        json.dump(content_variables, f)
