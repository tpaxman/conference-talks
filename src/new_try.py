from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


# open Chrome to the start page (the latest driver for Chrome 87 is sitting in the project folder)

browser = webdriver.Chrome()
browser.implicitly_wait(20)
browser.get(VOLUMES_URL)

def get_citationindex(browser):
    """
    Gets the name of the citationindex element that contains the links of interest.

    The links will be in either 'citationindex' or 'citationindex2' but it is not clear which will be the correct one
    This script waits until they both load and finds the one that has the links in it and returns the name of the ID.
    """

    CITATION_ID_NAMES = ['citationindex', 'citationindex2']

    # Gets the HTML associated with both citation index elements and attempts to find links inside
    def get_links_list(browser):
        citation_id_elems = [browser.find_element_by_id(x).get_attribute('innerHTML') for x in CITATION_ID_NAMES]
        citation_id_soups = [BeautifulSoup(x, features="lxml") for x in citation_id_elems]
        links_list = [name for name, soup in zip(CITATION_ID_NAMES, citation_id_soups) if soup.find_all('a')]
        return links_list

    # This runs until the page has actually loaded and the links are found inside the proper citationindex element
    links_list = []
    while not links_list:
        links_list = get_links_list(browser)

    # the name of the citation index element is returned (i.e. 'citationindex' or 'citationindex2')
    citationindex = links_list[0]
    return citationindex


# def get_links(javascript_command):
#
#     citation_data = soup.find(id=citation_id_str)
#     for x in citation_data.find_all('a'):
#         print(x.getText())

    # # to get the linke
    # a = [x for x in BeautifulSoup(browser.page_source).find(id='citationindex2').find_all('a') if
    #      ('getFilter' in x.get('onclick')) and (not x.find('span'))]
    #
    # # to get the refcounters on the last step
    # a = [x for x in BeautifulSoup(browser.page_source).find(id='citationindex2').find_all(class_='refcounter')]
    #
    # refcounters = [x for x in citation_data.find_all(class_='refcounter') if x.has_attr('onclick')]


# Locate the scripture pane on the left side of the page

# It seems to change between whether 'citationindex' or 'citationindex2' has the data
# so this chooses the non-empty one

# voltitle = citation_data.find(class_='volumetitle').getText()

# this is necessary because the center column also has 'refcounter' tags that are not wanted, so we keep only
# those with the 'onclick' attribute.
# data = [(x.get('onclick'),  # contains IDs for the talk and the reference
#          x.find(class_='reference').getText(),  # contains date and author
#          x.find(class_='talktitle').getText())  # contains the title
#         for x in citation_data.find_all(class_='refcounter') if x.has_attr('onclick')]

# IDEAS:

# check to make sure volume title is right
#
