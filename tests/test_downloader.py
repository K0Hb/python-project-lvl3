#!/usr/bin/env python3
from page_loader import download
from page_loader.loader import formation_local_name, KnownError, load_files
import tempfile
import pytest
import os


URL_TEST = 'http://knopka.ush.ru/'

PATH_FIXTURES_MOCK_lINKS = {
    'tests/fixtures/before_test_page.html': 'http://knopka.ush.ru/',
    'tests/fixtures/test_css.css': 'http://knopka.ush.ru/stl_newstatus.css',
    'tests/fixtures/test_svg.svg': 'http://knopka.ush.ru/images/logo.svg',
}

LOCAL_PATH_NAME = (
    'knopka-ush-ru_files/knopka-ush-ru.html',
    'knopka-ush-ru_files/knopka-ush-ru-stl_newstatus.css',
    'knopka-ush-ru_files/knopka-ush-ru-images-logo.svg',
)


def test_downloader(requests_mock) -> None:
    with tempfile.TemporaryDirectory() as temp:
        for fixture, link in PATH_FIXTURES_MOCK_lINKS.items():
            with open(fixture, 'rb') as fixture_file:
                mocking_content = fixture_file.read()
            requests_mock.get(link, content=mocking_content)
        path_load_page = download(URL_TEST, temp)

        with open(os.path.join(temp, path_load_page)) as test_page:
            with open('tests/fixtures/after_test_page.html') as fixture_page:
                assert test_page.read() == fixture_page.read()

        local_files = [os.path.join(temp, file) for file in LOCAL_PATH_NAME]

        for fixture, local in zip(PATH_FIXTURES_MOCK_lINKS, local_files):
            with open(fixture, 'rb') as fixture_file:
                with open(local, 'rb') as load_file:
                    assert fixture_file.read() == load_file.read()


@pytest.mark.parametrize('URL, get_name,file_status, dir_status,', [
    ('https://github.com/K0Hb/python-project-lvl3',
     'github-com-K0Hb-python-project-lvl3.html', None, None),
    ('https://github.com/K0Hb/python-project-lvl3',
     'github-com-K0Hb-python-project-lvl3_files', None, True),
    ('https://github.com/K0Hb/python-project-lvl3.css',
     'github-com-K0Hb-python-project-lvl3.css', True, None)
])
def test_get_name(URL: str, get_name: str, dir_status, file_status) -> None:
    assert formation_local_name(URL, file=file_status,
                                dir=dir_status) == get_name


def test_load_files() -> None:
    with tempfile.TemporaryDirectory() as temp:
        link_for_test = 'https://github.com/K0Hb/python-project-lvl3'
        path = os.path.join(temp, formation_local_name(link_for_test, 'file'))
        load_files([(link_for_test, path)])
        assert os.path.isfile(path)


@pytest.mark.parametrize('URL, path, exception', [
    ('K0Hb.github.io/github.io/', '/fantom_path/', 'Wrong address!'),
    ('ht://K0Hb.github.io/github.io/', '/fantom_path/', 'Wrong address!'),
    ('http://httpbin.org/status/404', '/fantom_path/', 'Connection failed'),
    ('https://github.com/K0Hb/python-project-lvl3',
     'unreal_path_to_file', 'Your folder is incorrect')
])
def test_errors(URL: str, path: str, exception: str) -> None:
    with pytest.raises(KnownError) as e_info:
        download(URL, path)
    assert exception in str(e_info.value)
