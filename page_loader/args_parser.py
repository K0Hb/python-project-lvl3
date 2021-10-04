import argparse
import os


DEBUG, INFO, WARNING, ERROR, CRITICAL = \
    'debug', 'info', 'error', 'warning', 'critical'


def args_parser():
    parser = argparse.ArgumentParser(description='Loads the URL of the page\
         to a file at the specified PATH')
    parser.add_argument('--output', default=os.getcwd())
    parser.add_argument('URL')
    parser.add_argument(
          '-l', '--level',
          type=str, default=INFO,
          choices=[DEBUG, INFO, WARNING, ERROR, CRITICAL],
          help='level of logging')
    return parser.parse_args()
