from bs4 import BeautifulSoup
import requests

def remove_desc_tag(str):

    return str.replace("[Written by MAL Rewrite]","").strip()

def scrape_url(page_link, anime_id):
    page_response = requests.get(page_link, timeout=5)
    try :
        page_response.raise_for_status()
        # here, we fetch the content from the url, using the requests library
        page_content = BeautifulSoup(page_response.content, "html.parser")
        #we use the html parser to parse the url content and store it in a variable.
        title = page_content.find("span", itemprop="name").text
        print("Anime #" + str(anime_id) + ": " + title)
        description = page_content.find("span", itemprop="description").text
        description = remove_desc_tag(description)
        print("Synopsis: " + description)
        print()
    except:
        print("Something went wrong for anime #" + str(anime_id) + "\n")

def main():
    for i in range(1, 10):
        anime_id = i
        scrape_url('https://myanimelist.net/anime/' + str(anime_id), anime_id)

main()