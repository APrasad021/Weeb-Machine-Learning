from bs4 import BeautifulSoup
import requests

def get_desc(page):
    description = page.find("span", itemprop="description").text   
    return description.replace("[Written by MAL Rewrite]","").strip()

def get_title(page):
    return page.find("span", itemprop="name").text

# scrape information from sidebar
# TODO: Handle and clean specific items in the sidebar that have extra text
def get_information(page):
    info = {}
    sidebar = page.find("td", class_="borderClass")
    children = sidebar.find_all("div")
    for i in range(len(children)):
        child = children[i]
        key = child.find("span")
        if key in child:
                items = child.text.split(":")
                key = items[0].strip()
                value = items[1].strip()
                info[key] = value
    return info
def scrape_url(page_link, anime_id):
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
        information = get_information(page_content)
        anime_data.update(information)
        #TODO: write values to text file
        for key, value in anime_data.items():
                print(key + ": " + value)
    except Exception as e:
        print("Something went wrong for anime #" + str(anime_id) + "\n")
        print(str(e))

def main():
#     for i in range(1, 10):
#         anime_id = i
#         scrape_url('https://myanimelist.net/anime/' + str(anime_id), anime_id)

    # run on one url for testing script
    anime_id = 20
    anime_url = 'https://myanimelist.net/anime/' + str(anime_id)
    scrape_url(anime_url, anime_id)
main()