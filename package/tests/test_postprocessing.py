
import pytest
from pathlib import Path
import shutil
import itertools

from conftest import TEST_DIR

from masonry.postprocessors import (
    CombineFilePrefix,
    CombineFilePostfix,
    CombineCodePrefix,
    CombineCodePostfix
)


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
    postprocessor = CombineFilePostfix(pattern='_postfix')
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


def test_combine_file_snippets_postprocessor_postfix_no_file_suffix(tmpdir):

    # GIVEN a directory of files, with *_post and *_prefixes that match other named files.
    TEST_DATA = TEST_DIR / Path('example_templates/python_project/')
    input_files = [
        TEST_DATA / Path(r'pytest/{{cookiecutter.package_name}}/Makefile'),
        TEST_DATA / Path(r'conda/{{cookiecutter.package_name}}/Makefile_postfix')
    ]
    # Use a temporary directory for the processing
    dest_path = Path(tmpdir.strpath) / 'postprocessing'
    dest_path.mkdir()
    for fp in input_files:
        shutil.copy(str(fp), str(dest_path))

    # WHEN combining files using the postprocessing rules
    postprocessor = CombineFilePostfix(pattern='_postfix')
    postprocessor.apply(dest_path)

    # THEN File should be concatonated
    file1_text = input_files[0].read_text()
    file2_text = input_files[1].read_text()

    result_path = dest_path / 'Makefile'
    result = result_path.read_text()
    assert result[:len(file1_text)] == file1_text
    assert result[len(file1_text):] == file2_text

    # THEN *_prefix and *_postfix files hould be removed as part of the processing
    config_file_present = (result_path / 'Makefile_postfix').exists()
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
    postprocessor = CombineFilePrefix(pattern='_prefix')
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


ns = range(1, 6)
fix = ('prefix', 'postfix')


@pytest.mark.parametrize('n,fix', itertools.product(ns, fix))
def test_code_insertion(tmpdir, n, fix):

    # GIVEN original python code file and some new code to insert into it
    starting_filepath = TEST_DIR / Path(f'data/postprocessing_examples/input/test_code{n}.py')
    new_content_filepath = TEST_DIR / Path(f'data/postprocessing_examples/input/new_code_{fix}.py')

    # Use a temporary directory for the processing
    dest_path = Path(tmpdir.strpath) / 'postprocessing'
    dest_path.mkdir()
    for fp in [starting_filepath, new_content_filepath]:
        shutil.copy(str(fp), str(dest_path))

    starting_filepath_copy = dest_path / starting_filepath.name
    new_content_filepath_copy = dest_path / new_content_filepath.name

    # Rename so file pattern will match
    dest = starting_filepath_copy.with_name(starting_filepath.stem + f'_{fix}.py')
    shutil.move(str(new_content_filepath_copy), str(dest))

    # WHEN code is inserted
    if fix == 'prefix':
        postprocessor = CombineCodePrefix()
    elif fix == 'postfix':
        postprocessor = CombineCodePostfix()
    changed_files = postprocessor.apply(dest_path)

    # THEN the following files should be changed
    assert changed_files == [str(starting_filepath_copy)]

    # THEN result should have the code in the right place, with pre and post being before or after
    # the main body of the code, which is the part after inports and constants, but before the
    # if __name__ == __main__ clause, if present
    target_path = TEST_DIR / Path(f'data/postprocessing_examples/output/result{n}_{fix}.py')
    target = target_path.read_text()
    result = open(changed_files[0]).read()
    assert target == result

    # THEN *_prefix and *_postfix files hould be removed as part of the processing
    prefix_files_present = dest_path.glob(f'*_{fix}*')
    assert not list(prefix_files_present)

    # CLEANUP
    shutil.rmtree(str(dest_path))
