
from pathlib import Path
import pytest
import git
import json
import os

from conftest import TEST_DIR

from masonry.objects.cli import CLI


@pytest.fixture()
def init_project_path(tmpdir):

    # Setup a basic project
    temp_output_path = Path(tmpdir.strpath)
    template_path = TEST_DIR / 'example_templates' / 'python_project'

    # Set arguments
    args = f"init -o {temp_output_path} {template_path}"

    app = CLI(args=args)
    app.run()

    return app.project.location


def test_adding_single_project(init_project_path):

    # Set arguments
    args = f"add -o {init_project_path.as_posix()} pytest"

    app = CLI(args=args)
    app.run()

    # Check files were created
    files = [
        # '.git/',
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
        p = init_project_path / f
        assert p.exists()

    # Check requirements were postfixed
    target = "requests\nlogzero\npytest\npytest-cov\ncoverage\n"
    req_file = init_project_path / 'requirements.txt'
    result = req_file.read_text()

    assert result == target

    # Check MANIFEST was prefixed
    target = "graft tests\ngraft src\n"
    manifest_file = init_project_path / 'MANIFEST.in'
    result = manifest_file.read_text()

    assert result == target

    # # Check git repo was created and commits made
    # repo_dir = init_project_path
    # r = git.Repo(repo_dir.as_posix())
    # log = r.git.log(pretty='oneline').split('\n')
    # assert len(log) == 2
    # assert "Add 'pytest' template layer via stone mason." in log[0]
    # assert "Add 'package' template layer via stone mason." in log[1]


def test_adding_multiple_projects(init_project_path):

    # Set arguments
    args = f"add -o {init_project_path.as_posix()} conda"

    app = CLI(args=args)
    app.run()

    # Check files were created
    files = [
        # '.git/',
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
        p = init_project_path / f
        assert p.exists()

    # Check requirements were polulated
    target = "requests\nlogzero\npytest\npytest-cov\ncoverage\n"
    req_file = init_project_path / 'requirements.txt'
    result = req_file.read_text()

    assert result == target

    # Check MANIFEST was prefixed
    target = "graft tests\ngraft src\n"
    manifest_file = init_project_path / 'MANIFEST.in'
    result = manifest_file.read_text()

    assert result == target

    # Check git repo was created and commits made
    # repo_dir = init_project_path
    # r = git.Repo(repo_dir.as_posix())
    # log = r.git.log(pretty='oneline').split('\n')
    # assert len(log) == 3
    # assert "Add 'conda' template layer via stone mason." in log[0]
    # assert "Add 'pytest' template layer via stone mason." in log[1]
    # assert "Add 'package' template layer via stone mason." in log[2]
