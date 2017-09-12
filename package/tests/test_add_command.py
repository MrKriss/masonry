
from pathlib import Path
import pytest
import git
import json
import os

from conftest import TEST_DIR


@pytest.fixture(scope='module')
def init_base_project(tmpdir_factory):

    # Setup a basic project
    temp_output_path = tmpdir_factory.mktemp('base_package').strpath
    template_path = os.path.join(TEST_DIR, 'data', 'python-project')

    # Set arguments
    args = f"init -o {temp_output_path} {template_path}"

    from stonemason import main
    # Run from entry point
    main.main(args=args)

    cookiecutter_vars_path = os.path.join(template_path, "package", "cookiecutter.json")
    with open(cookiecutter_vars_path, 'r') as f:
        cookiecutter_vars = json.load(f)

    package_name = cookiecutter_vars['package_name']
    project_dir = os.path.join(temp_output_path, package_name)

    return project_dir


def test_adding_single_project(init_base_project):

    current_project_path = Path(init_base_project)

    # Set arguments
    args = f"add -o {current_project_path.as_posix()} pytest"

    from stonemason import main
    # Run from entry point
    main.main(args=args)

    # Check files were created
    files = [
        '.git/',
        '.mason',
        'MANIFEST.in',
        'README',
        'requirements.txt',
        'setup.py',
        'src/testpackage',
        'src/testpackage/__init__.py',
        'src/testpackage/main.py',
        'tests/test_foo.py'
    ]
    for f in files:
        p = current_project_path / f
        assert p.exists()

    # Check requirements were postfixed
    target = "requests\nlogzero\npytest\npytest-cov\ncoverage\n"
    req_file = current_project_path / 'requirements.txt'
    result = req_file.read_text()

    assert result == target

    # Check MANIFEST was prefixed
    target = "graft tests\ngraft src\n"
    manifest_file = current_project_path / 'MANIFEST.in'
    result = manifest_file.read_text()

    assert result == target

    # Check git repo was created and commits made
    repo_dir = current_project_path
    r = git.Repo(repo_dir.as_posix())
    log = r.git.log(pretty='oneline').split('\n')
    assert len(log) == 2
    assert "Add 'pytest' template layer via stone mason." in log[0]
    assert "Add 'package' template layer via stone mason." in log[1]


def test_adding_multiple_projects(init_base_project):

    current_project_path = Path(init_base_project)

    # Set arguments
    args = f"add -o {current_project_path.as_posix()} conda"

    from stonemason import main
    # Run from entry point
    main.main(args=args)

    # Check files were created
    files = [
        '.git/',
        '.mason',
        'MANIFEST.in',
        'README',
        'requirements.txt',
        'setup.py',
        'src/testpackage',
        'src/testpackage/__init__.py',
        'src/testpackage/main.py',
        'tests/test_foo.py',
        'recipes/testpackage/build.bat',
        'recipes/testpackage/build.sh',
        'recipes/testpackage/run_test.py',
        'recipes/testpackage/meta.yaml'
    ]
    for f in files:
        p = current_project_path / f
        assert p.exists()

    # Check requirements were polulated
    target = "requests\nlogzero\npytest\npytest-cov\ncoverage\n"
    req_file = current_project_path / 'requirements.txt'
    result = req_file.read_text()

    assert result == target

    # Check MANIFEST was prefixed
    target = "graft tests\ngraft src\n"
    manifest_file = current_project_path / 'MANIFEST.in'
    result = manifest_file.read_text()

    assert result == target

    # Check git repo was created and commits made
    repo_dir = current_project_path
    r = git.Repo(repo_dir.as_posix())
    log = r.git.log(pretty='oneline').split('\n')
    assert len(log) == 3
    assert "Add 'conda' template layer via stone mason." in log[0]
    assert "Add 'pytest' template layer via stone mason." in log[1]
    assert "Add 'package' template layer via stone mason." in log[2]
