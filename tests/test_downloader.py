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
        test_path_to_page = re.fullmatch(r'/tmp/.........../milk-com.html',
                                         path_page)
        assert path_page == test_path_to_page.group(0)
        assert os.path.isfile(path_page)


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


def test_load_files() -> None:
    with tempfile.TemporaryDirectory() as temp:
        link_for_test = 'https://github.com/K0Hb/python-project-lvl3'
        path = os.path.join(temp, generate_name(link_for_test, 'file'))
        load_files([(link_for_test, path)])
        assert os.path.isfile(path)


@pytest.mark.parametrize('URL, path, exception' ,[
    ('K0Hb.github.io/github.io/', '/fantom_path/', 'Wrong address!'),
    ('ht://K0Hb.github.io/github.io/', '/fantom_path/', 'Wrong address!'),
    ('http://httpbin.org/status/404', '/fantom_path/', 'Connection failed'),
    ['https://github.com/K0Hb/python-project-lvl3',
     'unreal_path_to_file', 'Your folder is incorrect']
])
def test_errors(URL: str, path: str, exception: str) -> None:
    with pytest.raises(KnownError) as e_info:
        download(URL, path)
    assert exception in str(e_info.value)
