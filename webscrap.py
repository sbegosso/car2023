import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import sys
from typing import List, Tuple, Optional

#input link
LINK = str(sys.argv[1])

#key words to search for
CAR_COMPANIES = [
    "Toyota", "Volkswagen", "General Motors", "GM", "Ford", "Honda", "BMW", "Mercedes-Benz", "Nissan",
    "Tesla", "Audi", "Hyundai","Kia", "Volvo", "Jaguar", "Land Rover", "Porsche", "Subaru", "Mazda",
    "Fiat", "Chrysler", "Mitsubishi", "Peugeot", "Renault", "Aston Martin", "Ferrari", "Lamborghini",
    "Rolls-Royce", "Bentley", "Maserati", "Bugatti","Alfa Romeo", "Lotus", "McLaren", "Mini", "GMC",
    "Buick", "Ram", "Jeep", "Lincoln", "Acura", "Suzuki","Dodge","Chevrolet","Cadillac","Infiniti",
    "Lexus","Abarth","Mahindra","Tata Motors","Great Wall Motors","BYD Auto","Geely","Chery",
    "SsangYong","Haval","Proton","Perodua","Isuzu","FAW Group","Changan Automobile","Brilliance Auto",
    "GAC Group","JAC Motors","Dongfeng Motor","Haima Automobile","Roewe","BAIC Group","Wuling Motors"
]
KEY_WORDS = [
    "investment", "acquire", "acquisition", 
    "partnership", "joint venture", "strategic alliance",
    "stake", "equity", "funding", "capital infusion", "financial backing", "venture capital",
    "shareholding", "merger", "subsidiary", "divestment", "divestiture", "capital raise", "invest",
    "investment portfolio", "capital investment", "financial investment", "private equity", "construct",
    "EV", "EVs", "vehicle"
]

class SiteText:
    """
    Class for converting the website to text for analyzing
    """
    link: str

    def __init__(self, link: str) -> None:
        """
        Constructor function

        Params:
            self.link
            self.site
            self.soup
            self.text_list
        """
        self.link = str(link)
        self.site = requests.get(link)

        content_type = self.site.headers.get('Content-Type')
        
        if 'xml' in content_type:
            self.soup = BeautifulSoup(self.site.content, features='xml')
        else:
            self.soup = BeautifulSoup(self.site.content, 'html.parser')

        all_text = self.soup.get_text()
        self.text_list = all_text.splitlines()
        for t in self.text_list[:]:
            stripped_text = t.strip()
            if not stripped_text:
                self.text_list.remove(t)

    def get_title(self) -> str:
        """
        Returns the title of the website
        """
        return self.soup.title.text
    
    def chk_for_keys(self, phrase: str) -> bool:
        """
        Checks if a given phrase contains any key words
        """
        words = phrase.split()
        for word in words:
            if word in CAR_COMPANIES or word.lower() in KEY_WORDS or '$' in word:
                return True
        return False

    @property
    def simple_tl(self) -> List[str]:
        """
        Removes all white space in a string that's not directly adjacent to a word
        for all strings in a list

        Inputs:
            None

        Returns (List[str]): the refined list on strings
        """
        for i, t in enumerate(self.text_list[:]):
            words = t.strip().split()
            self.text_list[i] = ' '.join(words)
        return self.text_list

    def search_for_key_words(self) -> List[str]:
        """
        Searches through the simple text lists for any key words or names of car companies \
        and then returns the phrases that they are found in
        """
        important_phrases = []
        for phrase in self.simple_tl:
            words = phrase.split()
            for word in words:
                if word in CAR_COMPANIES or word.lower() in KEY_WORDS\
                    or '$' in word:
                    important_phrases.append(phrase)
                    break
        return important_phrases

    def find_all_links(self) -> List[str]:
        """
        Creates a list of all the links in a soup

        Returns (List[str]): the list of all the links
        """
        anchor_tags = self.soup.find_all('a')
        links = [str(tag.get('href')) for tag in anchor_tags]
        new_links = []
        for l in links:
            if l[0] == '/':
                new_links.append(self.link[0: len(self.link) - 1] + l)
            elif l.__contains__(self.link):
                new_links.append(l)
        return new_links


if __name__ == "__main__":
    site_text = SiteText(LINK)
    print(site_text.get_title())