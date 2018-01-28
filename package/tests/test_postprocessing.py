
import pytest
from pathlib import Path
import shutil
import itertools

from conftest import TEST_DIR

from masonry.objects.postprocessors import CombinePostfixFileSnippets, CombinePrefixFileSnippets


def test_combine_file_snippets_postprocessor_postfix(tmpdir):

    # GIVEN a directory of files, with *_post and *_prefixes that match other named files.
    input_files = [
        TEST_DIR / Path('data/postprocessing_examples/input/config.ini'),
        TEST_DIR / Path('data/postprocessing_examples/input/config_postfix.ini')
    ]
    # Use a temporary directory for the processing
    dest_path = Path(tmpdir.strpath) / 'postprocessing'
    dest_path.mkdir()
    for fp in input_files:
        shutil.copy(str(fp), str(dest_path))

    # WHEN combining files using the postprocessing rules
    postprocessor = CombinePostfixFileSnippets(pattern='_postfix')
    postprocessor.apply(dest_path)

    # THEN config_prefix.ini should be prefixed to config.ini
    target_path = TEST_DIR / Path('data/postprocessing_examples/output/result_config_postfix.ini')
    target = target_path.read_text()
    result_path = dest_path / 'config.ini'
    result = result_path.read_text()
    print(result)
    assert target == result

    # THEN *_prefix and *_postfix files hould be removed as part of the processing
    config_file_present = (result_path / 'config_postfix.ini').exists()
    assert not config_file_present

    # CLEANUP
    shutil.rmtree(str(dest_path))


def test_combine_file_snippets_postprocessor_prefix(tmpdir):

    # GIVEN a directory of files, with *_post and *_prefixes that match other named files.
    input_files = [
        TEST_DIR / Path('data/postprocessing_examples/input/config.ini'),
        TEST_DIR / Path('data/postprocessing_examples/input/config_prefix.ini'),
    ]
    # Use a temporary directory for the processing
    dest_path = Path(tmpdir.strpath) / 'postprocessing'
    dest_path.mkdir()
    for fp in input_files:
        shutil.copy(str(fp), str(dest_path))

    # WHEN combining files using the postprocessing rules
    postprocessor = CombinePrefixFileSnippets(pattern='_prefix')
    postprocessor.apply(dest_path)

    # THEN config_prefix.ini should be prefixed to config.ini
    target_path = TEST_DIR / Path('data/postprocessing_examples/output/result_config_prefix.ini')
    target = target_path.read_text()
    result_path = dest_path / 'config.ini'
    result = result_path.read_text()
    assert target == result

    # THEN *_prefix and *_postfix files hould be removed as part of the processing
    config_file_present = (result_path / 'config_prefix.py').exists()
    assert not config_file_present

    # CLEANUP
    shutil.rmtree(str(dest_path))
