import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import sys
from typing import List, Tuple, Optional

#input link
link = str(sys.argv[1])

class SiteText:
    """
    Class for converting the website to text for analyzing
    """
    link: str

    def __init__(self, link: str) -> None:
        """
        Constructor function
        """
        self.site = requests.get(link)
        self.soup = BeautifulSoup(self.site.content, 'html.parser')

        all_text = self.soup.get_text()
        self.text_list = all_text.splitlines()
        for t in self.text_list[:]:
            stripped_text = t.strip()
            if not stripped_text:
                self.text_list.remove(t)

    def remove_whitespace(self) -> None:
        """
        Removes all white space in a string that's not directly adjacent to a word
        for all strings in a list

        Inputs:
            None

        Returns (None)
        """
        for i, t in enumerate(self.text_list[:]):
            words = t.strip().split()
            self.text_list[i] = ' '.join(words)

site_text = SiteText(link)
site_text.remove_whitespace()
print(len(site_text.text_list))