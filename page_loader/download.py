import requests
import os
import re
from requests.exceptions import HTTPError


def download(url: str, path: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')

    if checking_the_directory(path):


        write_text = response.text
        
        filepath = os.path.join(path, generate_name_file(url))

        creating_file_with_content(filepath, write_text)

    return filepath

def generate_name_file(url: str) -> str:
    del_http = re.sub('(https?:\/\/)','', url)
    del_simvol = re.sub('[^\w^\d]', '-', del_http)
    result = del_simvol + '.html'
    return result

def checking_the_directory(path: str) -> bool:
    if os.path.isdir(str(path)) == False:
        print(f"there is no directory for this {str(path)}")
        return False
    return True

def creating_file_with_content(filepath: str, write_text: str) -> None:
    with open(filepath, 'w') as file:
        file.write(write_text)