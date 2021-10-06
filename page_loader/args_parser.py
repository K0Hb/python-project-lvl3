#!/usr/bin/env python3
import argparse
import os


DEBUG, INFO, WARNING, ERROR, CRITICAL = \
    'debug', 'info', 'error', 'warning', 'critical'


def args_parser():
    parser = argparse.ArgumentParser(description='Loads the URL of the page\
         to a file at the specified PATH')
    parser.add_argument('-o', '--output', default=os.getcwd(), type=str,
                        help='folder for saving link')
    parser.add_argument(
          '-l', '--level',
          type=str, default=INFO,
          choices=[DEBUG, INFO, WARNING, ERROR, CRITICAL],
          help='level of logging')
    parser.add_argument('URL', type=str)
    return parser.parse_args()
