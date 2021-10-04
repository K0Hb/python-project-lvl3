#!/usr/bin/env python3
from page_loader.download import download, set_level, KnownError
from page_loader.args_parser import args_parser
import logging
import sys


def main():
    namespace = args_parser()
    set_level(namespace.level)
    try:
        download(namespace.URL, namespace.output)
    except KnownError as e:
        cause = e.__cause__
        exc_info = (cause.__class__, cause, cause.__traceback__)
        logging.error(str(e), exc_info=exc_info)
        sys.exit(1)


if __name__ == '__main__':
    main()
