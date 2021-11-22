#!/usr/bin/env python3
from page_loader.download import download
from page_loader.loader import changing_logging_lvel, KnownError
from page_loader.args_parser import args_parser
import logging
import sys


def main() -> None:
    namespace = args_parser()
    url = namespace.URL
    path = namespace.output
    level_log = namespace.level
    changing_logging_lvel(level_log)
    try:
        file_path = download(url, path)
        print(f'Page saved in {file_path}')
    except KnownError:
        logging.error('Error')
        sys.exit(1)
    except PermissionError:
        logging.error('Not enough access rights')
        sys.exit(1)
    except FileNotFoundError:
        logging.error('No such file or directory')
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
