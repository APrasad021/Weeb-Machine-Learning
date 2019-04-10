from bs4 import BeautifulSoup
import requests
# scrape top 1000 anime for testing

def scrape_top_anime_url(url):
    page_response = requests.get(url, timeout=5)
    try :
        page_content = BeautifulSoup(page_response.content, "html.parser")
        anime_entries = page_content.find_all('tr', {'class': 'ranking-list'})
        # get url of each row
        # TODO: write each anime id/url to a file
        for entry in anime_entries:
            entry_url = entry.find('td', {'class': 'title al va-t word-break'}).find('a', href=True)['href']
            print(entry_url)
        return anime_entries
    except Exception as e:
        if page_response.status_code == 404:
                print("Top anime page " + url + " does not exist")
        else:
                print("Something went wrong for url " + url)
                print(str(e))
        
    return []

def get_top_anime():
    top_anime = []
    #each page shows 50 anime, so scrape each page
    for i in range(0, 1000, 50):
        url = "https://myanimelist.net/topanime.php?limit=" + str(i)
        scraped_anime = scrape_top_anime_url(url)
get_top_anime()