from bs4 import BeautifulSoup
import requests
import re

# gets the synopsis of the anime
def get_desc(page):
    description = page.find("span", itemprop="description").text   
    return description.replace("[Written by MAL Rewrite]","").strip()

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
def scrape_url(page_link, anime_id):
    # TODO: Fix 429 error (too many requests for url)
    page_response = requests.get(page_link, timeout=5)
    try :
        anime_data = {}
        # if the anime doesn't exist, an error will be raised
        page_response.raise_for_status()
        # if anime exists, get the html from the page
        page_content = BeautifulSoup(page_response.content, "html.parser")
        # parse html content
        anime_data['Title'] = get_title(page_content)
        anime_data['Description'] = get_desc(page_content)
        information = get_sidebar_information(page_content)
        anime_data.update(information)
        #TODO: write values to file
        for key, value in anime_data.items():
                print(key)
                print(value)
                print("=====================")
    except Exception as e:
        if page_response.status_code == 404:
                print("Anime #" + str(anime_id) + " does not exist")
        else:
                print("Something went wrong for anime #" + str(anime_id) + "\n")
                print(str(e))

def main():
    for i in range(1, 10):
        anime_id = i
        scrape_url('https://myanimelist.net/anime/' + str(anime_id), anime_id)
        print("========================")
main()