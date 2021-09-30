from page_loader.download import download
import tempfile
import pathlib
import re


def test_downloader():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir_name = tmp    
        path_dir = pathlib.Path(tmp)
        path_file = download('http://milk.com/' , path_dir)
        assert_path = re.fullmatch('\/tmp\/...........\/milk-com-.html', path_file)
        assert path_file == assert_path.group(0)