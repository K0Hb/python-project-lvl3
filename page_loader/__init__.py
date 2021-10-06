from page_loader.loader import (load_page, generate_name,
                                checking_the_directory,
                                edit_links, saved,
                                load_files)
import os


def download(url: str, path: str) -> tuple:

    page = load_page(url)

    name_of_page = generate_name(url)
    path_to_page = os.path.join(path, name_of_page)
    name_of_folder = generate_name(url, 'directory')
    path_to_folder = os.path.join(path, name_of_folder)

    checking_the_directory(path_to_folder)

    changed_page, source_of_files = \
        edit_links(page, url, path_to_folder)

    saved(changed_page, path_to_page)

    load_files(source_of_files)

    return path_to_page
