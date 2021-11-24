#!/usr/bin/env python3
from page_loader import download
from page_loader.loader import name_formation, KnownError, load_files
import tempfile
import pytest
import os


def test_downloader(requests_mock) -> None:
    with tempfile.TemporaryDirectory() as temp:
        with open('tests/fixtures/before_test_page.html') as web_page:
            html_before = web_page.read()
        with open('tests/fixtures/after_test_page.html') as result_page:
            html_after = result_page.read()
        url_test = 'http://knopka.ush.ru/'
        requests_mock.get(url_test, text=html_before)
        requests_mock.get('http://knopka.ush.ru/images/logo.svg')
        requests_mock.get('http://knopka.ush.ru/stl_newstatus.css')
        path_load_page = download(url_test, temp)
        with open(os.path.join(temp, path_load_page)) as f:
            test_page = f.read()
            assert test_page == html_after
        css_path = os.path.join(temp, "knopka-ush-ru_files/"
                                      "knopka-ush-ru-stl_newstatus.css")
        html_path = os.path.join(temp, 'knopka-ush-ru.html')
        svg_path = os.path.join(temp, "knopka-ush-ru_files/"
                                      "knopka-ush-ru-images-logo.svg")
        assert os.path.exists(css_path)
        assert os.path.exists(svg_path)
        assert os.path.exists(html_path)


@pytest.mark.parametrize('URL, get_name,file_status, dir_status,', [
    ('https://github.com/K0Hb/python-project-lvl3',
     'github-com-K0Hb-python-project-lvl3.html', None, None),
    ('https://github.com/K0Hb/python-project-lvl3',
     'github-com-K0Hb-python-project-lvl3_files', None, True),
    ('https://github.com/K0Hb/python-project-lvl3.css',
     'github-com-K0Hb-python-project-lvl3.css', True, None)
])
def test_get_name(URL: str, get_name: str, dir_status, file_status) -> None:
    assert name_formation(URL, file=file_status, dir=dir_status) == get_name


def test_load_files() -> None:
    with tempfile.TemporaryDirectory() as temp:
        link_for_test = 'https://github.com/K0Hb/python-project-lvl3'
        path = os.path.join(temp, name_formation(link_for_test, 'file'))
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
