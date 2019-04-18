from bs4 import BeautifulSoup
import requests
import re
import csv
import json
from time import sleep
# scrape mal data of anime to be able to reference the data later

# gets the synopsis of the anime
def get_desc(page):
    if page.find("span", itemprop="description") != None:
        description = page.find("span", itemprop="description").text   
        return description.replace("[Written by MAL Rewrite]","").strip()
    return "No description has been added to this title."

# gets name of the anime
def get_title(page):
    return page.find("span", itemprop="name").text

# converts a comma separated string into a list of the items
def convert_str_to_list(str):
    return [x.strip() for x in str.split(',')]

# clean values from sidebar
def clean_value(key, value):
    if key in ['Genres', 'Studios', 'Producers', 'Licensors', 'Synonyms']:
        value = "N/A" if "None found" in value else convert_str_to_list(value)
    elif key in ['Score', 'Ranked']:
        value = "N/A" if "N/A" in value else re.findall(r"[-+]?\d*\.\d+|\d+", value)[0]
    elif key == 'Popularity':
        value = value.replace("#","")
    return value       

# scrape information from sidebar
def get_sidebar_information(page):
    info = {}
    # get sidebar element then get all the div tags in the sidebar
    sidebar = page.find("td", class_="borderClass")
    children = sidebar.find_all("div")
    for i in range(len(children)):
        child = children[i]
        # check if the div has information
        info_tag = child.find("span")
        if info_tag in child:
                # extract the information and add it to the dictionary
                items = child.text.split(":")
                key = items[0].strip()
                value = items[1].strip()
                value = clean_value(key, value)
                if "* Your list is public by default." not in key:
                        info[key] = value
    return info

# tries to scrape a potential mal anime entry webpage
def scrape_anime_url(page_link, anime_id):
    page_response = requests.get(page_link, headers = {'User-agent': 'your bot 0.1'})
    try :
        anime_data = {}
        # if the anime doesn't exist, an error will be raised
        page_response.raise_for_status()
        # if anime exists, get the html from the page
        page_content = BeautifulSoup(page_response.content, "html.parser")
        # parse html content
        anime_data['anime_id'] = anime_id
        anime_data['Exists'] = True
        anime_data['Title'] = get_title(page_content)
        anime_data['Description'] = get_desc(page_content)
        information = get_sidebar_information(page_content)
        anime_data.update(information)
        return anime_data
    # Error handling
    except Exception as e:
        if page_response.status_code == 404:
            return None
        else:
            print(str(e))
            return {'anime_id': anime_id, 'Exists': False, 'Description': str(e)}
            

# def write_valid_row(data):
#     with open('mal_db_data.json', 'a', encoding='utf-8') as fp:
#         json.dump(data, fp)

# def write_invalid_row(anime_id, error_str):
#     fieldnames = ['anime_id', 'Exists', 'Description']
#     with open('mal_db_data.json', 'a', encoding='utf-8') as fp:
#         json.dump({'anime_id': anime_id, 'Exists': False, 'Description': error_str}, fp)

def scrape_urls_from_file(filename):
    try:
        urls = open(filename, "r", encoding='utf-8').read().strip().split("\n")
        data = []
        for url in urls:
            anime_id = int(url.split("/")[-2])
            info = scrape_anime_url(url, anime_id)
            if info != None:
                data.append(info)
            sleep(.5)
        write_json_data(data, 'mal_db_data.json')
    except Exception as e:
        print(str(e))

def write_json_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(data, fp)

def main():
    data = []
    for i in range(1, 10):
        anime_id = i
        info = scrape_anime_url('https://myanimelist.net/anime/' + str(anime_id), anime_id)
        if info != None:
            data.append(info)

scrape_urls_from_file("top_anime_urls.txt")
