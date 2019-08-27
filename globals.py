import os
import datetime
import json
import re

def get_timestamp():
    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime('%Y-%m-%d %H-%M-%S')
    return timestamp

def get_current_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return current_path

def get_configs():
    with open('config.json') as raw_json:
        configs = json.loads(raw_json.read())

    return configs

def get_text_qualifier():
    configs = get_configs()
    text_qualifier = configs['data']['text qualifier']
    return text_qualifier

def get_delimiter():
    configs = get_configs()
    delimiter = configs['data']['delimiter']
    return delimiter
        
def get_landing_url():
    configs = get_configs()
    landing_url = configs['data']['landing_url']
    return landing_url

def get_landing_urls():
    configs = get_configs()
    landing_urls = configs['data']['landing_urls']
    return landing_urls

def get_header(delimiter):
    header_row_file = open('header.txt', 'r')
    header_row_contents = header_row_file.read()
    header_row_file.close()
    
    header = str(header_row_contents)
    header = header.replace('\n', delimiter)
    return header

def clean_page_text(text):
    text = str(text)
    text = re.sub(r'([^(\x00-\x7F)]|[\-\$\,\/]|(\& ))', '', text)
    return text