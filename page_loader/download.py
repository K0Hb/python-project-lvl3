from page_loader.loader import (load_page, formation_local_name,
                                create_directory,
                                edit_links_to_local, save_file,
                                load_files)
import os
import logging
from progress.bar import IncrementalBar


def download(url: str, path: str) -> tuple:
    bar = IncrementalBar('Loading page', max=5, suffix='%(percent)d%%')
    page = load_page(url)
    bar.next()
    name_of_page = formation_local_name(url)
    path_to_page = os.path.join(path, name_of_page)
    name_of_folder = formation_local_name(url, dir=True)
    path_to_folder = os.path.join(path, name_of_folder)
    bar.next()
    create_directory(path_to_folder)
    bar.next()
    changed_page, source_of_files = \
        edit_links_to_local(page, url, path_to_folder)
    bar.next()
    save_file(changed_page, path_to_page)
    bar.next()
    load_files(source_of_files)
    bar.next()
    bar.finish()
    logging.info('The page is saved')
    return path_to_page
