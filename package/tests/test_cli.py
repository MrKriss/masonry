

import pytest
import py

from pathlib import Path

from masonry.objects.app import App

from schema import SchemaError


@pytest.fixture
def project_templates_path():
    return (
        py.path.local(__file__)
        .dirpath()
        .join('example_templates/simple_project')
    )


def test_cli_init_arguments(project_templates_path, tmpdir):

    argument_string = f"init {project_templates_path.strpath} -o {tmpdir.strpath}"

    app = App(argument_string)
    args = app.args

    assert 'init' in args
    assert args['PROJECT'] == Path(project_templates_path.strpath)
    assert args['--output'] == Path(tmpdir.strpath)


def test_cli_init_runs(project_templates_path, tmpdir):

    argument_string = f"init {project_templates_path.strpath} -o {tmpdir.strpath}"

    app = App(argument_string)
    app.run()
