#!/usr/bin/env python3
from page_loader import download
from page_loader.loader import generate_name, KnownError, load_files
import tempfile
import pathlib
import re
import pytest
import os


def test_downloader() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path_dir = pathlib.Path(tmp)
        path_page = download('http://milk.com/', path_dir)
        assert_path_to_page = re.fullmatch(r'/tmp/.........../milk-com.html',
                                           path_page)
        assert path_page == assert_path_to_page.group(0)


@pytest.mark.parametrize('URL, get_name, dir_status, file_status', [
    ('https://github.com/K0Hb/python-project-lvl3',
     'github-com-K0Hb-python-project-lvl3.html', None, None),
    ('https://github.com/K0Hb/python-project-lvl3',
     'github-com-K0Hb-python-project-lvl3_files', True, None),
    ('https://github.com/K0Hb/python-project-lvl3.css',
     'github-com-K0Hb-python-project-lvl3.css', None, True)
])
def test_get_name(URL: str, get_name: str, dir_status, file_status) -> None:
    assert generate_name(URL, dir=dir_status, file=file_status) == get_name


def test_connection_failed() -> None:
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(KnownError) as e_info:
            download('http://httpbin.org/status/404', temp)
        assert 'Connection failed' in str(e_info.value)


def test_load_files() -> None:
    with tempfile.TemporaryDirectory() as temp:
        link_for_test = 'https://github.com/K0Hb/python-project-lvl3'
        path = os.path.join(temp, generate_name(link_for_test, 'file'))
        load_files([(link_for_test, path)])
        assert os.path.isfile(path)


def test_error_no_schema() -> None:
    with pytest.raises(KnownError) as e_info:
        download('K0Hb.github.io/github.io/', '/fantom_path/')
    assert 'Wrong address!' in str(e_info.value)


def test_error_invalid_schema() -> None:
    with pytest.raises(KnownError) as e_info:
        download('ht://K0Hb.github.io/github.io/', '/fantom_path/')
    assert 'Wrong address!' in str(e_info.value)


def test_error_200() -> None:
    with pytest.raises(KnownError) as e_info:
        download('http://httpbin.org/status/404', '/fantom_path/')
    assert 'Connection failed' in str(e_info.value)


def test_error_umreal_folder() -> None:
    with pytest.raises(KnownError) as e_info:
        download('https://github.com/K0Hb/python-project-lvl3',
                 'unreal_path_to_file')
    assert 'Your folder is incorrect' in str(e_info.value)
