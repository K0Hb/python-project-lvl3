#!/usr/bin/env python3
from page_loader.download import download
from page_loader.args_parser import args_parser


def main():
    namespace = args_parser()
    print(download(namespace.URL, namespace.output))
    
if __name__ == '__main__':
    main()