from bs4 import BeautifulSoup
import requests
import json

def get_watched_anime(username):
    page_link = 'https://myanimelist.net/animelist/' + username
    page_response = requests.get(page_link, timeout=5)
    try :
        anime_data = {}
        page_content = BeautifulSoup(page_response.content, "html.parser")
        anime_entries = json.loads((page_content.find('table', attrs={'data-items' : True})['data-items']))
        anime_status = ["Watching", "Completed", "On Hold", "Dropped", "idk", "Plan to Watch"]
        # TODO: Tweak anime anime entries if needed
        for entry in anime_entries:
            print(entry['anime_title'], entry['anime_id'], anime_status[entry['status']-1], entry['score']) 
        return anime_entries
    except Exception as e:
        if page_response.status_code == 404:
                print("Username " + username + " does not exist")
        else:
                print("Something went wrong for username " + str(username) + "\n")
                print(str(e))


def main():
    user = "Enter MAL Username here"
    anime_ids = get_watched_anime(user)
main()