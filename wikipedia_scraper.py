import requests
from bs4 import BeautifulSoup
import re
import json
import time

root_url = "https://country-leaders.onrender.com/"
status_url = "status"
countries_endpoint = "countries"
cookies_endpoint = "cookie"
leaders_endpoint = "leaders"

pattern = r"\s{2,}" # regex to match multpile whitespaces in the text

leaders_data = {}

session = requests.Session() #create a session

# function to refresh cookies if they expire
def refresh_cookies():
    response = session.get(root_url + cookies_endpoint)
    if response.status_code == 200:
        session.cookies.update(response.cookies) #keep session authetincated for future requests
    else:
        print(f"Failed to get cookie: {response.status_code}")
        
# get the status
def get_status():
    response = session.get(root_url + status_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get status: {response.status_code}")
        return None

# function to get the list of countries
def get_countries():
    response = session.get(root_url + countries_endpoint)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        refresh_cookies()
        return get_countries()
    else:
        print(f"Failed to get countries: {response.status_code}")
        return None

# function to get leaders
def get_leaders(country):
    response = session.get(root_url + leaders_endpoint, params={"country": country})
    
    if response.status_code == 403:
        refresh_cookies()
        response = session.get(root_url + leaders_endpoint, params={"country": country})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get leaders for {country}: {response.status_code}")
        return None            


#function to get first paragraph
def get_first_paragraph(wikipedia_url):
    headers = {"User-Agent": "Mozilla/5.0"} #needed by wiki
    response = session.get(wikipedia_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    container = (soup.find("div", {"class": "mw-content-ltr mw-parser-output"}) or soup.find("div", {"class": "mw-parser-output"}))
    first_paragraph = ""
    for p in container.find_all("p"):
        if p.text.strip():
            first_paragraph = p.text
            break
    first_paragraph = re.sub(pattern, " ", first_paragraph)
    return first_paragraph


#function to updat leaders data with first paragraph
def update_leaders_data():
    for country in get_countries():
        leaders_data[country] = get_leaders(country)
        for leader in leaders_data[country]:
            leader["first_paragraph"] = get_first_paragraph(leader["wikipedia_url"])
        time.sleep(1) # to avoid overwhelming the server
update_leaders_data()        
        

#function to export data to json
def export_to_json(filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(leaders_data, f, ensure_ascii=False, indent=4)
