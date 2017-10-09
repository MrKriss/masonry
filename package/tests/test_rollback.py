
from pathlib import Path
import pytest
import git
import json
import os

from conftest import TEST_DIR

from stonemason import main


@pytest.fixture(scope='module')
def init_simple_project(tmpdir_factory):

    # Setup a basic project
    temp_output_path = Path(tmpdir_factory.mktemp('simple_project').strpath)
    template_path = TEST_DIR / 'example_templates' / 'breaking_project'

    # Set arguments
    args = f"init -o {temp_output_path} {template_path}"

    from stonemason import main
    # Run from entry point
    main.main(args=args)

    cookiecutter_vars_path = os.path.join(template_path, "first_layer", "cookiecutter.json")
    with open(cookiecutter_vars_path, 'r') as f:
        cookiecutter_vars = json.load(f)

    project_name = cookiecutter_vars['project_name']
    project_dir = temp_output_path / project_name

    return project_dir


def test_rollback_when_error_in_pre_hook(init_simple_project):

    # GIVEN an initialised project
    project_dir = init_simple_project

    # WHEN a template is added that causes an error
    args = f"add -o {project_dir} breaking_pre_hook"
    with pytest.raises(Exception):
        main.main(args=args)

    # THEN only the original files should be present
    target = set([
        project_dir / 'file_from_layer_1.txt',
        project_dir / '.mason',
        project_dir / '.git',
    ])
    result = set(project_dir.iterdir())
    assert result == target

    # THEN original file should be unchanged
    target = '123456'
    result_file = project_dir / 'file_from_layer_1.txt'
    result = result_file.read_text()
    assert result == target


def test_rollback_when_error_in_post_hook(init_simple_project):

    # GIVEN an initialised project
    project_dir = init_simple_project

    # WHEN a template is added that causes an error
    args = f"add -o {project_dir} breaking_post_hook"
    with pytest.raises(Exception):
        main.main(args=args)

    # THEN only the original files should be present
    target = set([
        project_dir / 'file_from_layer_1.txt',
        project_dir / '.mason',
        project_dir / '.git',
    ])
    result = set(project_dir.iterdir())
    assert result == target

    # THEN original file should be unchanged
    target = '123456'
    result_file = project_dir / 'file_from_layer_1.txt'
    result = result_file.read_text()
    assert result == target


def test_rollback_when_error_in_variable_name(init_simple_project):

    # GIVEN an initialised project
    project_dir = init_simple_project

    # WHEN a template is added that causes an error
    args = f"add -o {project_dir} breaking_variable_name"
    with pytest.raises(Exception):
        main.main(args=args)

    # THEN only the original files should be present
    target = set([
        project_dir / 'file_from_layer_1.txt',
        project_dir / '.mason',
        project_dir / '.git',
    ])
    result = set(project_dir.iterdir())
    assert result == target

    # THEN original file should be unchanged
    target = '123456'
    result_file = project_dir / 'file_from_layer_1.txt'
    result = result_file.read_text()
    assert result == target


def test_rollback_when_init_project(tmpdir_factory):

    # GIVEN a temp directory and template to initialise
    temp_output_path = Path(tmpdir_factory.mktemp('empty_project').strpath)
    template_path = TEST_DIR / 'example_templates' / 'breaking_project'

    # WHEN a new project is initialised that causes an error
    args = f"init -o {temp_output_path} {template_path}/breaking_variable_name"
    with pytest.raises(Exception):
        main.main(args=args)

    # THEN the directory should be empty
    target = set([])
    result = set(temp_output_path.iterdir())
    assert result == target
