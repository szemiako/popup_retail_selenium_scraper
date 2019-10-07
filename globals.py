# -*- coding: utf-8 -*-
# v1.5

import os
import datetime
import json
import re

def get_timestamp():
    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H-%M-%S")
    return timestamp

def get_current_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return current_path

def get_configs():
    with open("config.json") as raw_json:
        configs = json.loads(raw_json.read())
    return configs

def get_text_qualifier():
    configs = get_configs()
    text_qualifier = configs["data"]["text qualifier"]
    return text_qualifier

def get_delimiter():
    configs = get_configs()
    delimiter = configs["data"]["delimiter"]
    return delimiter
        
def get_landing_url():
    configs = get_configs()
    landing_url = configs["data"]["landing_url"]
    return landing_url

def get_landing_urls():
    configs = get_configs()
    landing_urls = configs["data"]["landing_urls"]
    return landing_urls

def get_header():
    configs = get_configs()
    headers = configs["data"]["headers"]
    return headers

def clean_page_text(text):
    text = str(text)
    text = re.sub(r"([^(\x00-\x7F)]|[\-\$\,\/]|(\& ))", "", text)
    return text

def simple_error(error_type, url = "", notes = ""):
    url = str(url)

    errors = {
        "posting_opening_error" : "{error_type}: Error at retrieving data on URL '"'{url}'"'.\n".format(error_type = error_type, url = url),
        "landing_page_navigation_error" : "{error_type}: Error at opening xpath '"'{xpath}'"' from URL '"'{url}'"'.\n".format(error_type = error_type, xpath = notes, url = url),
        "next_page_error" : "{error_type}: Error navigating to next page from URL '"'{url}'"'.\n".format(error_type = error_type, url = url),
        "page_retrival_error" : "{error_type}: Error on URL '"'{url}'"' retrieving number of pages. Indication that there is only one (1) page with {total_cards} listings.\n".format(error_type = error_type, url = url, total_cards = notes),
        "parsing_error" : "{error_type}: Error with parsing page data:\n'"'{page}'"'\n".format(error_type = error_type, page = notes),
        "" : "Unclassified error. URL, if provided: '"'{url}'"'\nNotes, if provided: '"'{notes}'"'\n".format(url = url, notes = notes)
    }

    error_message = errors[error_type]

    return error_message
