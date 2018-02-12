
from pathlib import Path
import pytest
import git
import json
import os

from conftest import TEST_DIR
from masonry.objects.project import Project

from cookiecutter.exceptions import FailedHookException, UndefinedVariableInTemplate


# @pytest.fixture(scope='module')
# def init_simple_project(tmpdir_factory):

#     # Setup a basic project
#     temp_output_path = Path(tmpdir_factory.mktemp('simple_project').strpath)
#     template_path = TEST_DIR / 'example_templates' / 'breaking_project'

#     # Set arguments
#     args = f"init -o {temp_output_path} {template_path}"

#     from masonry import main
#     # Run from entry point
#     main.main(args=args)

#     cookiecutter_vars_path = os.path.join(template_path, "first_layer", "cookiecutter.json")
#     with open(cookiecutter_vars_path, 'r') as f:
#         cookiecutter_vars = json.load(f)

#     project_name = cookiecutter_vars['project_name']
#     project_dir = temp_output_path / project_name

#     return project_dir


@pytest.fixture(scope='module')
def init_simple_project(tmpdir_factory):

    temp_output_path = Path(tmpdir_factory.mktemp('simple_project').strpath)
    template_path = TEST_DIR / 'example_templates' / 'breaking_project'

    # Set arguments
    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project = Project(template_path)
    project.initialise(output_dir=temp_output_path, variables=init_variables)

    return project


def test_rollback_when_error_in_pre_hook(init_simple_project):

    # GIVEN an initialised project
    project = init_simple_project

    # WHEN adding a template that has a failing prehook
    with pytest.raises(FailedHookException):
        project.add_template(name='breaking_pre_hook', variables={})

    # THEN only the original files should be present
    project_name = project.template_variables['project_name']
    root_dir = project.location / project_name
    target = set([
        root_dir / 'file_from_layer_1.txt',
        # root_dir / '.mason',
        # root_dir / '.git',
    ])
    result = set(root_dir.iterdir())
    assert result == target

    # THEN original file should be unchanged
    target = '123456'
    result_file = root_dir / 'file_from_layer_1.txt'
    result = result_file.read_text()
    assert result == target


@pytest.mark.xfail
def test_rollback_when_error_in_post_hook(init_simple_project):

    # GIVEN an initialised project
    project_dir = init_simple_project

    # WHEN a template is added that causes an error
    args = f"add -o {project_dir} breaking_post_hook"
    with pytest.raises(FailedHookException):
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


@pytest.mark.xfail
def test_rollback_when_error_in_variable_name(init_simple_project):

    # GIVEN an initialised project
    project_dir = init_simple_project

    # WHEN a template is added that causes an error
    args = f"add -o {project_dir} breaking_variable_name"
    with pytest.raises(UndefinedVariableInTemplate):
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


@pytest.mark.xfail
def test_rollback_when_init_project(tmpdir_factory):

    # GIVEN a temp directory and template to initialise
    temp_output_path = Path(tmpdir_factory.mktemp('empty_project').strpath)
    template_path = TEST_DIR / 'example_templates' / 'breaking_project'

    # WHEN a new project is initialised that causes an error
    args = f"init -o {temp_output_path} {template_path}/breaking_variable_name"
    with pytest.raises(UndefinedVariableInTemplate):
        main.main(args=args)

    # THEN the directory should be empty
    target = set([])
    result = set(temp_output_path.iterdir())
    assert result == target
