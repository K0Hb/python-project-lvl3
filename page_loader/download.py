import requests
import os
import re
import logging
from progress.bar import IncrementalBar
import magic
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.args_parser import DEBUG, INFO, WARNING, ERROR, CRITICAL


class KnownError(Exception):
    pass


def modification_level(level_logging: str) -> None:
    dict_of_level = {DEBUG: logging.DEBUG,
                     WARNING: logging.WARNING,
                     ERROR: logging.ERROR,
                     CRITICAL: logging.CRITICAL,
                     INFO: logging.INFO,
                     }
    return logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                               filename='my.log',
                               filemode='w',
                               level=dict_of_level[level_logging])


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

    return name_of_page, name_of_folder, path_to_page, path_to_folder


def generate_name(url: str, status=None) -> str:
    link = url.rstrip('/')
    o = urlparse(link)
    name = o.netloc + o.path
    if status == 'file':
        name, extension = os.path.splitext(name)
    final_name = ''
    for letter in name:
        letter_new = re.sub(r'\W', '-', letter)
        final_name += letter_new
        if len(final_name) >= 50:
            break
    if status == 'file':
        final_name += extension
    elif status == 'directory':
        final_name += '_files'
    else:
        final_name += '.html'
    return final_name


def checking_the_directory(path: str) -> None:
    logging.info('Сhecking the directory')
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except IOError as e:
            raise KnownError('Your folder is incorrect') from e


def saved(changed_page: str, path_to_page: list, mode='w') -> None:
    logging.info('Saving page')
    try:
        with open(path_to_page, mode) as file:
            file.write(changed_page)
    except IOError as e:
        raise KnownError('Your folder is incorrect') from e


def load_page(link: str) -> str:
    logging.info('Loading page')
    try:
        page = requests.get(link)
        page.raise_for_status()
    except (requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema) as e:
        raise KnownError('Wrong address!') from e
    except requests.exceptions.HTTPError as e:
        raise KnownError('Connection failed') from e
    except requests.exceptions.ConnectionError as e:
        raise KnownError('Connection error') from e
    return page.text


def load_files(source: list) -> None:
    logging.info('Loading links')
    bar = IncrementalBar('Loading links', max=len(source))
    for link, path_to_extra_file in source:
        try:
            r = requests.get(link)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise KnownError('Connection failed') from e
        except requests.exceptions.ConnectionError as e:
            raise KnownError('Connection error') from e
        text_types = {'text/html', 'text/css', 'text/javascript'}
        mime_type = magic.from_buffer(r.content, mime=True)
        mode, data = ('w', r.text) if mime_type in text_types \
            else ('wb', r.content)
        with open(path_to_extra_file, mode) as f:
            f.write(data)
        bar.next()
    bar.finish()


def edit_links(page: str, url: str, path_to_folder_for_files: str) -> tuple:
    logging.info('Changing page')
    soup = BeautifulSoup(page, "lxml")
    links = soup.find_all(["script", "img", "link"])
    stop_prefix = ['http', 'www']
    result = []
    attr = ''
    link = ''
    for tag in links:
        if 'href' in tag.attrs:
            attr = 'href'
            link = tag['href']
        elif 'src' in tag.attrs:
            attr = 'src'
            link = tag['src']
        if attr != '':
            if all(not link.startswith(prefix)
                   for prefix in stop_prefix):
                link = link.lstrip('/')
                path = os.path.join(url, link)
                path_to_extra_file = \
                    os.path.join(
                        path_to_folder_for_files,
                        generate_name(path, 'file'))
                tag[attr] = path_to_extra_file
                result.append((path, path_to_extra_file))
    changed_page = (soup.prettify("utf-8")).decode('utf-8')
    return changed_page, result
