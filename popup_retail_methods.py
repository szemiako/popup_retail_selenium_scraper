# -*- coding: utf-8 -*-
# v1.5

import re
import globals

def list_index_value(value, data_to_search):
    for i, datum in enumerate(data_to_search, 0):
        if value in datum:
            index_value = tuple([i, datum])
            break
        else:
            index_value = None
    return index_value

def no_space(string_pattern, no_space_string):
    delimiter = globals.get_delimiter()
    text_qualifier = globals.get_text_qualifier()
    no_spaces = re.findall(string_pattern, no_space_string)
    for ns in no_spaces: no_space_string = re.sub(ns, ns[0] + delimiter + " " + ns[1], no_space_string)
    delimited_string = text_qualifier + str(no_space_string) + text_qualifier
    return delimited_string

def is_ignored(header):
    headers_to_ignore = [
        "title",
        "location"
    ]
    if header in headers_to_ignore: return True
    return False

def parse_listing_data(str_data, headers):
    data = str_data.split("\n")

    delimiter = globals.get_delimiter()
    text_qualifier = globals.get_text_qualifier()

    headers = [header for header in headers]
    num_col = len(headers)
    
    data_row = [None] * num_col

    p = 0
    is_more_photos = re.match("[0-9]", data[0])
    if is_more_photos is not None: p = 1

    # Title of listing
    data_row[0] = data[p]

    # Location / Neighborhood
    data_row[1] = data[p + 1]

    j = 0
    k = 0

    for i, header in enumerate(headers, 0):
        # matches = [x for x in data if headers in x]
        # matches = list(filter(lambda x: h in x, data))

        if is_ignored(header) == True:
            continue

        matches = list_index_value(header, data)       
        if matches == None:
            data_row[i] = None
            continue
       
        # Trying to avoid situations where the header is per week
        # but per weekend day gets also flagged.
        # if header == "per week" and "end day" in matches[1]:
        #     data_row[i] = None
        #     continue

        if "Amenities" in matches[1] or "Ideal Uses" in matches[1]:
            k = matches[0] + 1
            data_row[i] = no_space("[a-z][A-Z]", data[k])
            k = 0

        elif "About this space" in matches[1]:
            about = []
            j = int(matches[0]) + 1
            is_next = re.fullmatch("^[A-Za-z]{1,} [A-Za-z]{1,}$", data[j])
            while is_next is None:
                about.append(data[j])
                j = j + 1
                is_next = re.fullmatch("^[A-Za-z]{1,} [A-Za-z]{1,}$", data[j])
            data_row[i] = text_qualifier + " ".join(about) + text_qualifier

        elif ":" in matches[1]:
            data_row[i] = re.sub("(^[A-Za-z]{1,} [A-Za-z]{1,}: )|(^[A-Za-z]{1,}: )", "", matches[1])

        elif "rate" in matches[1]:
            # data_row[i] = re.sub("([A-Za-z]{1,} [A-Za-z]{1,}$)|([A-Za-z]{1,} [A-Za-z]{1,} [A-Za-z]{1,}$)", "", matches[1])
            k = matches[0] + 1
            data_row[i] = re.match(r"[0-9]{1,}\.[0-9]{2}", data[k]).string
            k = 0
    
    data_row = ["NULL" if datum is None else str(datum) for datum in data_row]
    data_row_str = delimiter.join(data_row)
    data_row_str = str(data_row_str)

    return data_row_str

def get_xpath_span(page_text):
    pricing_info = re.findall("[A-Za-z]{1,} .{0,3}[0-9]{1,} [A-Za-z]{1,} [A-Za-z]{1,}", page_text)
    xpath_span = len(pricing_info)
    return xpath_span

def build_xpaths(page_text):
    # The first xpath is always a different format than the other xpaths.
    page_xpaths = ["(.//*[normalize-space(text()) and normalize-space(.)='Loading Listings'])[1]/following::div[3]"]

    # This pattern matches "From HKD3200 per day"
    pricing_info = re.findall("[A-Za-z]{1,} .{0,3}[0-9]{1,} [A-Za-z]{1,} [A-Za-z]{1,}", page_text)
    num_prices = len(pricing_info)

    # This pattern matches "18 m  Subayat Jaya"
    is_place = re.findall("\n[0-9]{1,} (?=.)[ A-Za-z]{1,}\n", page_text)
    num_places = len(is_place)

    # Less 1 to account for the first, different string.
    total_listings = num_prices - 1

    # Places should always be counted correctly (due to specificity of the string pattern).
    # Therefore, we always subtract prices from places (as there may be listings with no prices, e.g. "Price: Upon Reuqest")
    price_upon_request = abs(num_places - num_prices)

    # Iterant + 1 because range starts at 0.

    # DEBUGGING ONLY
    total_listings = 4
    for i in range(total_listings):
        xpath = "(.//*[normalize-space(text()) and normalize-space(.)='per day'])[{i_1}]/following::div[2]".format(i_1 = i + 1)
        page_xpaths.append(xpath)

    # for i in range(total_listings):
    #     xpath = "(.//*[normalize-space(text()) and normalize-space(.)='per day'])[{i_1}]/following::div[2]".format(i_1 = i + 1)
    #     page_xpaths.append(xpath)

    # for j in range(price_upon_request):
    #     xpath = "(.//*[normalize-space(text()) and normalize-space(.)='Price: Upon Request'])[{j_1}]/following::div[2]".format(j_1 = j + 1)
    #     page_xpaths.append(xpath)

    return page_xpaths

def dep2_build_xpaths(page_text):
    # This pattern matches "From HKD3200 per day"
    pricing_info = re.findall("[A-Za-z]{1,} .{0,3}[0-9]{1,} [A-Za-z]{1,} [A-Za-z]{1,}", page_text)
    num_prices = len(pricing_info)

    # This pattern matches "18 m  Subayat Jaya"
    is_place = re.findall("\n[0-9]{1,} (?=.)[ A-Za-z]{1,}\n", page_text)
    num_places = len(is_place)

    # Less 1 to account for the first, different string.
    

    # Places should always be counted correctly (due to specificity of the string pattern).
    # Therefore, we always subtract prices from places (as there may be listings with no prices, e.g. "Price: Upon Reuqest")
    price_upon_request = abs(num_places - num_prices)

    # The first xpath is always a different format than the other xpaths.
    total_listings = num_prices - 1
    page_xpaths = [("(.//*[normalize-space(text()) and normalize-space(.)='Loading Listings'])[1]/following::div[", 15)]
    
    for i in range(total_listings):
        page_xpaths.append(("(.//*[normalize-space(text()) and normalize-space(.)='per day'])[{i_1}]/following::div[".format(i_1 = i + 1), 14))
    
    for j in range(price_upon_request):
        page_xpaths.append(("(.//*[normalize-space(text()) and normalize-space(.)='Price: Upon Request'])[{j_1}]/following::div[".format(j_1 = j + 1), 14))

    # page_xpaths = ["(.//*[normalize-space(text()) and normalize-space(.)='Loading Listings'])[1]/following::div[16]"]
    # for i in range(total_listings): page_xpaths.append("(.//*[normalize-space(text()) and normalize-space(.)='View Details'])[{i_1}]/following::div[14]".format(i_1 = i + 1))
    return page_xpaths

def dep1_build_xpaths(page_text):
    # The first xpath is always a different format than the other xpaths.
    page_xpaths = ["(.//*[normalize-space(text()) and normalize-space(.)='Loading Listings'])[1]/following::div[3]"]

    postings = re.finditer("([A-Za-z0-9 ]{1,}){1,}[A-Za-z0-9 ]{1,}", page_text, re.MULTILINE)
    ignore = 0

    for p, posts in enumerate(postings, 1):
        post = str(posts.group())
        
        # This pattern matches "From HKD3200 per day"
        pricing_info = re.search("[A-Za-z]{1,}(?=.)[0-9]{1,} [A-Za-z]{1,} [A-Za-z]{1,}", post)
        
        # This pattern matches "18 m  Subayat Jaya"
        is_place = re.fullmatch("^[0-9]{1,} (?=.)[ A-Za-z]{1,}$", post)

        if pricing_info is not None or is_place is not None: ignore += 1
   
    # Less 1 to account for the first, different string.
    total_postings = (p - ignore) - 1

    for i in range(total_postings):
        xpath = "(.//*[normalize-space(text()) and normalize-space(.)='per day'])[" + str(i + 1) + "]/following::div[2]"
        page_xpaths.append(xpath)

    return page_xpaths
