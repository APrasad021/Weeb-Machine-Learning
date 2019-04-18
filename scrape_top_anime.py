from bs4 import BeautifulSoup
import requests
# gets urls of the top 4000 anime for scraping

def scrape_top_anime_urls(url):
    page_response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
    try :
        page_content = BeautifulSoup(page_response.content, "html.parser")
        anime_entries = page_content.find_all('tr', {'class': 'ranking-list'})
        # get url of each row
        urls = []
        for entry in anime_entries:
            entry_url = entry.find('td', {'class': 'title al va-t word-break'}).find('a', href=True)['href']
            urls.append(entry_url)
        return urls
    # Error handling
    except Exception as e:
        if page_response.status_code == 404:
                print("Top anime page " + url + " does not exist")
        else:
                print("Something went wrong for url " + url)
                print(str(e))
        
    return []

def write_urls_to_file(urls):
    # write a url to each line of the file
    with open('top_anime_urls.txt', 'w', encoding="utf-8") as f:
        for item in urls:
            f.write("%s\n" % item)

def get_top_anime():
    top_anime_urls = []
    #each page shows 50 anime, so scrape each page
    for i in range(0, 4000, 50):
        url = "https://myanimelist.net/topanime.php?limit=" + str(i)
        scraped_urls = scrape_top_anime_urls(url)
        top_anime_urls.extend(scraped_urls)
    
    # comment out print line if you only want a list of the urls
    write_urls_to_file(top_anime)
    return top_anime_urls

get_top_anime()