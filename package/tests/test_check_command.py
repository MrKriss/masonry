
from pathlib import Path
import pytest
import git
import json

from conftest import TEST_DIR

from masonry.objects.app import App


def test_init_with_project():

    # Set arguments
    args = f"check {TEST_DIR}/example_templates/python_project"

    app = App(args=args)
    app.run()

    dirs = [d.name for d in Path(app.check_dir).iterdir() if d.is_dir()]
    dirs.sort()

    assert dirs == ['conda', 'pytest']

    # Check files were created for pytest package
    package_name = 'testpackage'
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
    ]

    for f in files:
        p = app.check_dir / 'pytest' / package_name / f
        assert p.exists()

    # Check files were created for conda
    package_name = 'testpackage'
    files = [
        # '.git/',
        '.mason',
        'MANIFEST.in',
        'Makefile',
        'README',
        'requirements.txt',
        'dev_environment.yml',
        'setup.py',
        'src/testpackage',
        'src/testpackage/__init__.py',
        'src/testpackage/main.py',
        'recipes/testpackage/build.bat',
        'recipes/testpackage/build.sh',
        'recipes/testpackage/meta.yaml',
        'recipes/testpackage/run_test.py',
        'tests/test_foo.py',
    ]

    for f in files:
        p = app.check_dir / 'conda' / package_name / f
        assert p.exists()
