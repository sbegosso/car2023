import urllib.parse
import requests
import os
from bs4 import BeautifulSoup as bs
import sys
import csv
from datetime import date
import re

#input link
LINK1 = str(sys.argv[1])
LINK2 = str(sys.argv[2])
LINK3 = str(sys.argv[3])

LINKS = [LINK1, LINK2, LINK3]

#key words to search for
KEY_WORDS = [
    " ev ", " evs ", "vehicle", "toyota", "volkswagen", "general motors", "gm", "ford", "honda", "bmw",
    "tesla", "audi", "hyundai","kia", "volvo", "jaguar", "land rover", "porsche", "subaru", "mazda",
    "fiat", "chrysler", "mitsubishi", "peugeot", "renault", "aston martin", "ferrari", "lamborghini",
    "rolls-royce", "bentley", "maserati", "bugatti","alfa romeo", "lotus", "mclaren", "mini", "gmc",
    "buick", "ram", "jeep", "lincoln", "acura", "suzuki","dodge","chevrolet","cadillac","infiniti",
    "lexus","abarth","mahindra","tata motors","great wall motors","byd auto","geely","chery",
    "ssangyong","haval","proton","perodua","isuzu","faw group","changan automobile","brilliance auto",
    "gac group","jac motors","dongfeng motor","haima automobile","roewe","baic group","wuling motors",
    "mercedes-benz", "nissan", "electric", "battery", "plant", "expand", "report", "production",
    "investment", "acquire", "acquisition","stake", "equity", "funding", "shareholding", "merger", "invest", "$"
]
ANTI_KEY_WORDS = [
    "rumor", "rumors", "rumored", "guide", " sec ", "potential", "maybe", "podcast", "cute", "ebike"
]

def go(link):
    """
    The function where the the bfs search through the links exists
    """
    print("SEARCHING THROUGH: {}".format(link))
    important_links = set()
    visited_links = set()
    queue = [(link, 0)]

    #bfs begins here
    while len(queue) > 0:
        current_url, depth = queue.pop(0)
        visited_links.add(current_url)

        req = get_request(current_url)
        soup = bs(req.content, "html5lib")

        #checks the title for key words
        if chk_title(soup.title):
            important_links.add((current_url, soup.title))

        #extract all the links on the page
        all_links = find_all_links(link, soup)

        if depth < 1:
            new_depth = depth + 1
            for url in all_links:
                if url not in visited_links and url[len(url) - 1] == '/':
                    queue.append((url, new_depth))

    print("SEARCH IS COMPLETE FOR: {}".format(link))
    return important_links

def multi_go(links):
    """
    Same as go method, just takes in multiple links
    """
    all_urls = set()
    for link in links:
        all_urls.update(go(link))
    return all_urls

def chk_title(title):
    """
    Checks a string to see if it includes any key words
    """
    str_title = str(title).lower()
    word_lst = []
    for good_word in KEY_WORDS:
        if good_word in str_title:
            word_lst.append(good_word)
    for bad_word in ANTI_KEY_WORDS:
        if bad_word in str_title:
            return False
    return len(word_lst) > 1 and len(str_title.split()) > 4
        

def get_request(link):
    """
    Opens a connection to the specified URL and if successful
    read the data.
    """
    if is_absolute_url(link):
        try:
            r = requests.get(link)
            if r.status_code == 404 or r.status_code == 403:
                print("NUM 1")
                r = None
        except Exception:
            # fail on any kind of error
            r = None
    else:
        print("NUM2")
        r = None
    return r

def is_absolute_url(link):
    """
    Is url an absolute URL?
    """
    if link == "":
        return False
    return urllib.parse.urlparse(link).netloc != ""
    
def find_all_links(link, soup):
        """
        Creates a list of all the links in a soup
        """
        anchor_tags = soup.find_all('a')
        links = [str(tag.get('href')) for tag in anchor_tags]
        new_links = []
        for l in links:
            if l[0] == '/':
                new_links.append(link[0: len(link) - 1] + l)
            elif l.__contains__(link):
                new_links.append(l)
        return new_links

def create_csv(data):
    """
    Creates a csv file based on the important links found
    """
    curr_date = date.today()
    formatted_curr_date = curr_date.strftime('%m/%d/%Y')

    filename = '{}_scraped_links.csv'.format(formatted_curr_date)
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)

def to_string(important_links):
    """
    Formats all the websites in a cleaner manner in the text box below
    """
    for url, title in important_links:
        try:
            cleaned_title = re.sub(r"<title>|</title>", "", title)
            print("Title: {}".format(cleaned_title))
        except:
            print("Title: {}".format(title))
        print("URL: {}".format(url))
        print("-----")

if __name__ == "__main__":
    important_links = multi_go(LINKS)
    print(important_links)
    #create_csv(important_links)