import argparse
import os


def args_parser():
    parser = argparse.ArgumentParser(description='Loads the URL of the page\
         to a file at the specified PATH')
    parser.add_argument('--output', default=os.getcwd())
    parser.add_argument('URL')
    return parser.parse_args()
