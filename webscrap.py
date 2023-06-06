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
    "Toyota", "Volkswagen", "General Motors", "Ford", "Honda", "BMW", "Mercedes-Benz", "Nissan",
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
        self.link = link
        self.site = requests.get(link)
        self.soup = BeautifulSoup(self.site.content, 'html.parser')

        all_text = self.soup.get_text()
        self.text_list = all_text.splitlines()
        for t in self.text_list[:]:
            stripped_text = t.strip()
            if not stripped_text:
                self.text_list.remove(t)

    def remove_whitespace(self) -> List[str]:
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
        
        """
        important_phrases = []
        cleaned_text = self.remove_whitespace()
        for phrase in cleaned_text:
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
                new_links.append(self.link + l)
        return new_links


site_text = SiteText(LINK)
print(site_text.search_for_key_words())