
from pathlib import Path

from masonry.cli import MasonrySchema


import pytest


@pytest.mark.parametrize('path', ['~', '.', '..', '../..'])
def test_schema_handels_home_and_relative_paths(path):

    args = {
        '--help': False,
        '--output': path,
        '--version': False,
        '-v': False,
        'PROJECT': path,
        'TEMPLATE': [],
        'add': False,
        'check': False,
        'init': True
    }

    args = MasonrySchema(args).validate()

    assert args['PROJECT'] == Path(path).expanduser().resolve()


@pytest.mark.parametrize('path', ['foo', 'a/b/c', '\2\5/6/f//3', '//2!£$%6@/\/\/'])
def test_schema_handels_non_path_strings(path):

    args = {
        '--help': False,
        '--output': '.',
        '--version': False,
        '-v': False,
        'PROJECT': path,
        'TEMPLATE': [],
        'add': False,
        'check': False,
        'init': True
    }

    with pytest.raises(SystemExit) as e:
        args = MasonrySchema(args).validate()

    assert "PROJECT path does not exist." in str(e.value)
