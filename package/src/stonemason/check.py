
import json

import py.path

from stonemason.resolution import create_dependency_graph, resolve
from stonemason.template import add_template, initialise_project

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


# def test_bake_all_template_layers(cookies, template_orders):
#     """Test for 'cookiecutter-template'."""

#     for idx, (layer, deps) in enumerate(template_orders.items()):
#         cookies._count = idx
#         for dep in deps:
#             result = cookies.bake(template=str(dep))
#             cookies._count = idx

#             assert result.exit_code == 0
#             assert result.exception is None


# ===================================Pytest Cookies ==========================================

# -*- coding: utf-8 -*-


# USER_CONFIG = u"""
# cookiecutters_dir: "{cookiecutters_dir}"
# replay_dir: "{replay_dir}"
# """


# class Result(object):
#     """Holds the captured result of the cookiecutter project generation."""

#     def __init__(self, exception=None, exit_code=0, project_dir=None):
#         self.exception = exception
#         self.exit_code = exit_code
#         self._project_dir = project_dir

#     @property
#     def project(self):
#         if self.exception is None:
#             return py.path.local(self._project_dir)
#         return None

#     def __repr__(self):
#         return '<Result {}>'.format(
#             self.exception and repr(self.exception) or self.project
#         )


# class Cookies(object):
#     """Class to provide convenient access to the cookiecutter API."""

#     def __init__(self, template, output_factory, config_file):
#         self._default_template = template
#         self._output_factory = output_factory
#         self._config_file = config_file
#         self._counter = 0

#     def _new_output_dir(self):
#         dirname = 'bake{:02d}'.format(self._counter)
#         output_dir = self._output_factory(dirname)
#         self._counter += 1
#         return output_dir

#     def bake(self, extra_context=None, template=None):
#         exception = None
#         exit_code = 0
#         project_dir = None

#         if template is None:
#             template = self._default_template

#         try:
#             project_dir = cookiecutter(
#                 template,
#                 no_input=True,
#                 extra_context=extra_context,
#                 output_dir=str(self._new_output_dir()),
#                 config_file=str(self._config_file)
#             )
#         except SystemExit as e:
#             if e.code != 0:
#                 exception = e
#             exit_code = e.code
#         except Exception as e:
#             exception = e
#             exit_code = -1

#         return Result(exception, exit_code, project_dir)


# @pytest.fixture(scope='session')
# def _cookiecutter_config_file(tmpdir_factory):
#     user_dir = tmpdir_factory.mktemp('user_dir')

#     cookiecutters_dir = user_dir.mkdir('cookiecutters')
#     replay_dir = user_dir.mkdir('cookiecutter_replay')

#     config_text = USER_CONFIG.format(
#         cookiecutters_dir=cookiecutters_dir,
#         replay_dir=replay_dir,
#     )
#     config_file = user_dir.join('config')

#     config_file.write_text(config_text, encoding='utf8')
#     return config_file


# @pytest.yield_fixture
# def cookies(request, tmpdir, _cookiecutter_config_file):
#     """Yield an instance of the Cookies helper class that can be used to
#     generate a project from a template.

#     Run cookiecutter:
#         result = cookies.bake(extra_context={
#             'variable1': 'value1',
#             'variable2': 'value2',
#         })
#     """
#     template_dir = request.config.option.template

#     output_dir = tmpdir.mkdir('cookies')
#     output_factory = output_dir.mkdir

#     yield Cookies(template_dir, output_factory, _cookiecutter_config_file)

#     output_dir.remove()


# def pytest_addoption(parser):
#     group = parser.getgroup('cookies')
#     group.addoption(
#         '--template',
#         action='store',
#         default='.',
#         dest='template',
#         help='specify the template to be rendered',
#         type='string',
#     )
