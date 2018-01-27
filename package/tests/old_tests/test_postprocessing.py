""" Tests for code and text insertion postprocessing
"""

import pytest
from pathlib import Path
import shutil
import itertools


from conftest import TEST_DIR

from masonry.postprocess import insert_code, combine_file_snippets


ns = range(1, 6)
kinds = ('pre', 'post')


@pytest.mark.parametrize('n,kind', itertools.product(ns, kinds))
def test_code_insertion(n, kind):

    # GIVEN original python code file and some new code to insert into it
    original_path = TEST_DIR / Path(f'data/postprocessing_examples/input/test_code{n}.py')
    new_code_path = TEST_DIR / Path(f'data/postprocessing_examples/input/new_code.py')
    target_path = TEST_DIR / Path(f'data/postprocessing_examples/output/result{n}_{kind}.py')

    # WHEN code is inserted
    result = insert_code(new_code_path, original_path, kind=f'{kind}fix')

    # THEN result should have the code in the right place, with pre and post being before or after
    # the main body of the code, which is the part after inports and constants, but before the
    # if __name__ == __main__ clause, if present
    target = target_path.read_text()
    assert target == result


def test_combine_file_snippets(tmpdir):

    # GIVEN a directory of files, with *_post and *_prefixes that match other named files.
    input_files = [
        TEST_DIR / Path('data/postprocessing_examples/input/config.ini'),
        TEST_DIR / Path('data/postprocessing_examples/input/config_postfix.ini'),
        TEST_DIR / Path('data/postprocessing_examples/input/main.py'),
        TEST_DIR / Path('data/postprocessing_examples/input/main_prefix.py')
    ]
    # Use a temporary directory for the processing
    dest_path = Path(tmpdir.strpath) / 'postprocessing'
    dest_path.mkdir()
    for fp in input_files:
        shutil.copy(str(fp), str(dest_path))

    # WHEN combining files using the postprocessing rules
    combine_file_snippets(tmpdir.strpath)

    # THEN main_prefix.py should be prefixed to main.py
    target_path = TEST_DIR / Path('data/postprocessing_examples/output/result1_pre.py')
    target = target_path.read_text()
    result_path = dest_path / 'main.py'
    result = result_path.read_text()
    assert target == result

    # THEN config_prefix.ini should be prefixed to config.ini
    target_path = TEST_DIR / Path('data/postprocessing_examples/output/result_config.ini')
    target = target_path.read_text()
    result_path = dest_path / 'config.ini'
    result = result_path.read_text()
    assert target == result

    # THEN *_prefix and *_postfix files hould be removed as part of the processing
    main_file_present = (result_path / 'main_prefix.py').exists()
    assert not main_file_present
    config_file_present = (result_path / 'config_postfix.py').exists()
    assert not config_file_present

    # CLEANUP
    shutil.rmtree(str(dest_path))
