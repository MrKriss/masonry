""" Tests for code and text insertion postprocessing
"""

import pytest
from pathlib import Path
import shutil
import itertools


from conftest import TEST_DIR

from stonemason.postprocess import insert_code, combine_file_snippets


ns = range(1, 6)
kinds = ('pre', 'post')


@pytest.mark.parametrize('n,kind', itertools.product(ns, kinds))
def test_code_insertion(n, kind):

    original_path = TEST_DIR / Path(f'data/code_examples/test_code{n}.py')
    new_code_path = TEST_DIR / Path(f'data/code_examples/new_code.py')
    target_path = TEST_DIR / Path(f'data/code_examples/result{n}_{kind}.py')

    target = target_path.read_text()
    result = insert_code(new_code_path, original_path, kind=f'{kind}fix')

    assert target == result


def test_combine_file_snippets(tmpdir):

    # Setup
    sample_project_path = TEST_DIR / Path(f'data/code_examples/miniproject/')
    dest_project_path = Path(tmpdir.strpath) / 'miniproject'
    shutil.copytree(sample_project_path.as_posix(), dest_project_path.as_posix())

    # Run
    combine_file_snippets(tmpdir.strpath)

    # Test
    target_path = TEST_DIR / Path('data/code_examples/result1_pre.py')
    target = target_path.read_text()
    result_path = Path(tmpdir.strpath) / Path('miniproject/main.py')
    result = result_path.read_text()
    assert target == result

    target_path = TEST_DIR / Path('data/code_examples/result_config.ini')
    target = target_path.read_text()
    result_path = Path(tmpdir.strpath) / Path('miniproject/config.ini')
    result = result_path.read_text()
    assert target == result
