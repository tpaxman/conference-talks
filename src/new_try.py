from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import sys

VOLUMES_URL = 'https://scriptures.byu.edu/#::fNYNY7267e401'


def get_book_url(book_num):
    book_hexnum = hex(book_num)[2:].zfill(3)
    return VOLUMES_URL + book_hexnum


def get_chapter_url(book_num, chapter_num):
    book_url = get_book_url(book_num)
    chapter_hexnum = hex(chapter_num)[2:].zfill(2)
    chapter_url = book_url + chapter_hexnum
    return chapter_url


def get_verse_url(book_num, chapter_num, verse_num):
    chapter_url = get_chapter_url(book_num, chapter_num)
    verse_url = chapter_url + str(verse_num)
    return verse_url


# open Chrome webdriver (the latest driver for Chrome 87 is sitting in the project folder)
browser = webdriver.Chrome()

# configure browser to wait for stuff to load
browser.implicitly_wait(20)

# Locate the scripture pane on the left side of the page
verse_url = get_verse_url(101, 11, 4)
browser.get(verse_url)
page_source = browser.page_source
soup = BeautifulSoup(page_source, features="lxml")

# It seems to change between whether 'citationindex' or 'citationindex2' has the data
# so this chooses the non-empty one
citation_id_str = [x for x in ('citationindex', 'citationindex2') if soup.find(id=x).find_all(class_='refcounter')][0]
citation_data = soup.find(id=citation_id_str)

voltitle = citation_data.find(class_='volumetitle').getText()


# this is necessary because the center column also has 'refcounter' tags that are not wanted, so we keep only
# those with the 'onclick' attribute.
data = [(x.get('onclick'),  # contains IDs for the talk and the reference
         x.find(class_='reference').getText(),  # contains date and author
         x.find(class_='talktitle').getText())  # contains the title
        for x in citation_data.find_all(class_='refcounter') if x.has_attr('onclick')]

# IDEAS:

# check to make sure volume title is right
#