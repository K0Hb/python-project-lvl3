#!/usr/bin/env python3
import requests
import os
import re
import logging
from progress.bar import IncrementalBar
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
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


def generate_name(url: str, file=None, dir=None) -> str:
    logging.info('Сreating a name')
    link = url.rstrip('/')
    o = urlparse(link)
    name = o.netloc + o.path
    if file:
        name, extension = os.path.splitext(name)
    final_name = ''
    for letter in name:
        letter_new = re.sub(r'\W', '-', letter)
        final_name += letter_new
        if len(final_name) >= 50:
            break
    if file:
        final_name += extension
    elif dir:
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


def saved(changed_page: str and bytes, path_to_page: str, mode='wb') -> None:
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
        data = r.content
        saved(data, path_to_extra_file, mode='wb')
        bar.next()
    bar.finish()


def edit_links(page: str, url: str, path_to_folder_for_files: str) -> tuple:
    tags = {'link': 'href', 'img': 'src', 'script': 'src'}
    dir_path, dir_name = os.path.split(path_to_folder_for_files)
    soup = BeautifulSoup(page, 'html.parser')
    result = []

    def check_local(element) -> bool:
        link = element.get(tags[element.name])
        netloc_first = urlparse(url).netloc
        netloc_second = urlparse(urljoin(url, link)).netloc
        return netloc_first == netloc_second

    elements = filter(lambda string_http: check_local(string_http),
                      soup.find_all(list(tags)))
    for element in elements:
        tag = tags[element.name]
        link = urljoin(url, element.get(tag))
        if len(link.split('.')[-1]) >= 5:
            resource_path = os.path.join(dir_name, generate_name(link))
        else:
            resource_path = os.path.join(dir_name,
                                         generate_name(link, file=True))
        element[tag] = resource_path
        result.append((link, os.path.join(dir_path, resource_path)))
        changed_page = soup.prettify("utf-8")
    return changed_page, result
