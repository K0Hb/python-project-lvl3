from page_loader.download import download, generate_name, KnownError, load_files
import tempfile
import pathlib
import re
import pytest
import os


def test_downloader():
    with tempfile.TemporaryDirectory() as tmp:   
        path_dir = pathlib.Path(tmp)
        path_page, path_to_folder = download('http://milk.com/' , path_dir)[2:]
        assert_path_to_page = re.fullmatch('\/tmp\/...........\/milk-com.html', path_page)
        assert_path_to_folder = re.fullmatch('\/tmp\/...........\/milk-com_files', path_to_folder)
        assert path_page == assert_path_to_page.group(0)
        assert path_to_folder == assert_path_to_folder.group(0)


@pytest.mark.parametrize('URL, get_name, status', [
    ('https://github.com/K0Hb/python-project-lvl3',
    'github-com-K0Hb-python-project-lvl3.html', None),
    ('https://github.com/K0Hb/python-project-lvl3',
    'github-com-K0Hb-python-project-lvl3_files', 'directory'),
    ('https://github.com/K0Hb/python-project-lvl3.css',
    'github-com-K0Hb-python-project-lvl3.css', 'file')
])
def test_get_name(URL, get_name, status):
    assert generate_name(URL, status) == get_name


def test_connection_failed():
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(KnownError) as e_info:
            download('http://httpbin.org/status/404', temp)
        assert 'Connection failed' in str(e_info.value)

def test_load_files():
    with tempfile.TemporaryDirectory() as temp:
        link_for_test = 'https://github.com/K0Hb/python-project-lvl3'
        path = os.path.join(temp, generate_name(link_for_test, 'file'))
        load_files([(link_for_test, path)])
        assert os.path.isfile(path)