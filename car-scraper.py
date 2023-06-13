import urllib.parse
import requests
import os
from bs4 import BeautifulSoup as bs
import sys
import csv
from datetime import date
import re

FIELDS = ['Date Accessed', 'URL', 'Title']

CURR_DATE = date.today()
F_CURR_DATE = CURR_DATE.strftime('%m-%d-%Y')

#key words to search for
KEY_WORDS = [
    " ev", " ev ", " evs ", "vehicle", "toyota", "volkswagen", "general motors", "gm", "ford", "honda", "bmw",
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
    "rumor", "rumors", "rumored", "guide", " sec ", "potential", "maybe", "podcast", "cute", "ebike", "alibaba", 
    "concept", "explorer"
]

#input links
n = int(input("Enter the number of inputs: "))
INPUT_LINKS = []

for i in range(n):
    value = input("Enter input {}: ".format(i + 1))
    INPUT_LINKS.append(value)

print(INPUT_LINKS)

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

        print(current_url)

        try:
            req = get_request(current_url)
            soup = bs(req.content, "html5lib")

            #checks the title for key words
            if chk_title(soup.title):
                important_links.add((F_CURR_DATE, current_url, soup.title.string))

            if depth < 1:
                new_depth = depth + 1
                
                #extract all the links on the page
                all_links = find_all_links(link, soup)
                
                for url in all_links:
                    if url not in visited_links and url[len(url) - 1] == '/':
                        queue.append((url, new_depth))
        except:
            pass

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
    return len(word_lst) > 1 and len(str_title.split()) > 5
        

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
            if l.__contains__(link):
                new_links.append(l)
            elif l[0] == '/':
                new_links.append(link[0: len(link) - 1] + l)
        return new_links

def clean_data(data):
    """
    Takes input from the output of the go() method and converts it from a 
    set of tuples to a list of lists. Also cleans up the titles.
    """
    list_of_lists = [list(t) for t in data]
    return list_of_lists

def create_csv(fields, rows):
    """
    Turning the above data into a csv file... kind of an experiment for now
    """
    curr_date = date.today()
    formatted_curr_date = curr_date.strftime('%m-%d-%Y')

    filename = '{}_scraped_urls.csv'.format(formatted_curr_date)
    with open(filename, 'w', newline = '') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
        csvwriter.writerow(INPUT_LINKS)

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
    important_links = multi_go(INPUT_LINKS)
    print(clean_data(important_links))
    create_csv(FIELDS, clean_data(important_links))