
import json

import py.path

from masonry.resolution import create_dependency_graph, resolve
from masonry.template import add_template, initialise_project

from contextlib import redirect_stdout
from clint.textui import puts, indent, colored


def check_templates(template_collection_path, template=None, logfile='log'):

    default_template = get_default_template(template_collection_path)

    template_orders = get_template_orders(template_collection_path)

    tmpdir = py.path.local.mkdtemp().mkdir('check')

    # Rediect stdout to a file temporarily
    logfile = open(logfile, 'a')

    if default_template in template_orders:
        del template_orders[default_template]

    error_log = []

    for layer, deps in template_orders.items():

        if default_template in deps:
            deps.remove(default_template)

        output_dir = tmpdir.mkdir(layer)
        puts(colored.yellow(f'Testing Layer: {layer}'))
        puts(colored.yellow(f'Installing: {deps}'))

        project_dir = initialise_project(template_collection_path,
                                         output_dir=str(output_dir),
                                         interactive=False,
                                         stream=logfile.write)
        for dep in deps:
            try:
                puts(f'Adding layer: {dep}')
                add_template([dep], project_dir, interactive=False, stream=logfile.write)
            except Exception as e:
                msg = f'{e} encountered on adding "{dep}" to project for layer "{layer}"'
                error_log.append(msg)

    if error_log:
        puts(colored.red("Errors were encountered:"))
        with indent(4):
            for err in error_log:
                puts(colored.red(err))
    else:
        puts(colored.green("All template layers created without error"))


def get_template_orders(template_collection_path):
    """Return the orders in which to apply templates for all layers"""

    template_collection_path = py.path.local(template_collection_path)

    metadata = template_collection_path.join('metadata.json')

    layers = [x.basename for x in template_collection_path.listdir()
              if x.isdir() and x.basename != '__pycache__']

    g = create_dependency_graph(metadata, layers)

    orders = {}
    for layer in layers:
        orders[layer] = [x.name for x in resolve(g[layer])]

    return orders


def get_default_template(template_collection_path):

    template_collection_path = py.path.local(template_collection_path)

    # Find default template
    metadata = json.load(template_collection_path.join('metadata.json'))
    default_template = metadata['default']

    return default_template
