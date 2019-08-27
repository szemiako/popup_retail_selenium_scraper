import re
import globals

def list_index_value(value, data_to_search):
    for i, datum in enumerate(data_to_search, 0):
        if value in datum:
            index_value = tuple([i, datum])
            break
        else:
            index_value = 'NULL'
    
    return index_value

def no_space(string_pattern, no_space_string):
    delimiter = globals.get_delimiter()
    text_qualifier = globals.get_text_qualifier()
    
    no_spaces = re.findall(string_pattern, no_space_string)
    for ns in no_spaces: no_space_string = re.sub(ns, ns[0] + delimiter + ns[1], no_space_string)
    delimited_string = text_qualifier + str(no_space_string) + text_qualifier
    return delimited_string

def get_listing_data(str_data, headers):
    headers_to_ignore = [
        'title',
        'location'
    ]

    delimiter = globals.get_delimiter()
    num_col = headers.count(delimiter) + 1
    headers = headers.split(delimiter)
    
    data = str_data.split('\n')
    data_row = ['NULL'] * num_col
    data_row_str = ''

    # Title of listing
    # print(data[0])
    data_row[0] = data[0]

    # Location / Neighborhood
    data_row[1] = data[1]

    for i, header in enumerate(headers, 0):
        # matches = [x for x in data if headers in x]
        # matches = list(filter(lambda x: h in x, data))

        if header in headers_to_ignore: continue

        matches = list_index_value(header, data)       
        if matches == 'NULL':
            data_row[i] = matches
            continue

        # The following statements can be improvde upon:----
        # if header == 'per week' and 'end day' in matches[1]:
        #     data_row[i] = None
        #     continue
        
        if header == 'per week' and len(matches[1]) > len(header):
            data_row[i] = 'NULL'
            continue

        # if header == 'location': continue
        # --------------------------------------------------

        # includes size, space type, floor / access, rental capacity, min rental, max rental, ref_num
        # has_colon = re.match('(^[A-Za-z]{1,} [A-Za-z]{1,}: )|(^[A-Za-z]{1,}: )', matches[1])
        if ':' in matches[1]: has_colon = True
        
        # per day, per week, per weekend day, per month
        # doesn't appear to work...
        if 'per' in matches[1]: per_diem = True
        # per_diem = re.match('([A-Za-z]{1,} [A-Za-z]{1,}$)|([A-Za-z]{1,} [A-Za-z]{1,} [A-Za-z]{1,}$)', matches[1])

        if 'Amenities' in matches[1]:
            data_row[i] = no_space('[a-z][A-Z]', data[i + 1])

        elif 'Ideal Uses' in matches[1]:
            data_row[i] = no_space('[a-z][A-Z]', data[i + 1])
        
        elif 'About this space' in matches[1]:
            about = []
            j = int(matches[0])
            is_next = re.fullmatch('^[A-Za-z]{1,} [A-Za-z]{1,}$', data[j])
            while is_next is None:
                about.append(data[j])
                j = j + 1
                is_next = re.fullmatch('^[A-Za-z]{1,} [A-Za-z]{1,}$', data[j])
            data_row[i] = ' '.join(about)

        elif has_colon == True: data_row[i] = re.sub('(^[A-Za-z]{1,} [A-Za-z]{1,}: )|(^[A-Za-z]{1,}: )', '', matches[1])

        elif per_diem == True: data_row[i] = re.sub('([A-Za-z]{1,} [A-Za-z]{1,}$)|([A-Za-z]{1,} [A-Za-z]{1,} [A-Za-z]{1,}$)', '', matches[1])
    
    data_row_str = delimiter.join(data_row)
    data_row_str = str(data_row_str)

    return data_row_str

def build_xpaths(page_text):
    page_xpaths = []
    
    total_listings = re.findall('(\\n([A-Za-z]{1,} ){2,}[A-Za-z]{1,}\\n)', page_text)
    total_listings = len(total_listings)

    # The first xpath is always a different format than the other xpaths.
    xpath = '(.//*[normalize-space(text()) and normalize-space(.)="'"Loading Listings"'"])[1]/following::div[3]'
    page_xpaths.append(xpath)
    for i in range(total_listings):
        xpath = '(.//*[normalize-space(text()) and normalize-space(.)="'"per day"'"])[' + str(i + 1) + ']/following::div[2]'
        xpath = xpath.replace('"',"'")
        page_xpaths.append(xpath)

    return page_xpaths

# def depreciated_build_xpaths(page_text):
#     landing_page_list = page_text.split('\n')
#     page_xpaths = []
    
#     counter = 0
#     sp_counter = 0
#     new_counter = 0

#     for j in range(len(landing_page_list)):
#         special = re.fullmatch('^([A-Za-z]{1,})$|^([A-Za-z]{1,} [A-Za-z]{1,})$', landing_page_list[j])

#         if j + 1 > len(landing_page_list) - 1:
#             is_name = None
#         else:
#             is_name = re.fullmatch('([A-Za-z]{1,} ){2,}[A-Za-z]{1,}', landing_page_list[j + 1])

#         if special != None and is_name != None:
#             if landing_page_list[j] == 'Top Space':
#                 counter += 1
#                 xpath = '(.//*[normalize-space(text()) and normalize-space(.)="'"Top Space"'"])[' + str(counter) + ']/following::div[5]'
#                 xpath = xpath.replace('"',"'")

#                 page_xpaths.append(xpath)
#             elif landing_page_list[j] == 'Staff Pick':
#                 sp_counter += 1
#                 xpath = '(.//*[normalize-space(text()) and normalize-space(.)="'"Staff Pick"'"])[' + str(sp_counter) + ']/following::div[5]'
#                 xpath = xpath.replace('"',"'")
                
#                 page_xpaths.append(xpath)
#             elif landing_page_list[j] == 'New':
#                 new_counter += 1
#                 xpath = '(.//*[normalize-space(text()) and normalize-space(.)="'"New"'"])[' + str(new_counter) + ']/following::div[5]'
#                 xpath = xpath.replace('"',"'")
                
#                 page_xpaths.append(xpath)
#         elif special == None and is_name != None:
#             counter += 1
#             xpath = '(.//*[normalize-space(text()) and normalize-space(.)="'"per day"'"])[' + str(counter) + ']/following::div[11]'
#             xpath = xpath.replace('"',"'")
            
#             page_xpaths.append(xpath)
    
#     return page_xpaths