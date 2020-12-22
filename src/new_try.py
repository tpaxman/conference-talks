from bs4 import BeautifulSoup
from selenium import webdriver
import time

VOLUMES_URL = 'https://scriptures.byu.edu/#::fNYNY7267e401'


def get_citationindex(browser):
    """
    Gets the name of the citationindex element that contains the links of interest.
    The links will be in either 'citationindex' or 'citationindex2' but it is not clear which will be the correct one
    This script waits until they both load and finds the one that has the links in it and returns a bs4 Soup object.
    """

    def get_soup_list(browser):
        """Gets the HTML associated with both citation index elements and attempts to find links inside"""
        citation_id_names = ['citationindex', 'citationindex2']
        citation_id_elems = [browser.find_element_by_id(x).get_attribute('innerHTML') for x in citation_id_names]
        citation_id_soups = [BeautifulSoup(x, features="lxml") for x in citation_id_elems]
        soup_list = [soup for soup in citation_id_soups if soup.find_all('a')]
        return soup_list

    # This runs until the page has actually loaded and the links are found inside the proper citationindex element
    soup_list = []
    while not soup_list:
        soup_list = get_soup_list(browser)

    # the BeautifulSoup object of the citation index element is returned (i.e. for 'citationindex' or 'citationindex2')
    citationindex_soup = soup_list[0]
    return citationindex_soup


def dig_into_citations(browser, script=''):
    """
    Searches recursively through the scriptures website until it finds all talks for each of the citations
    """
    soup = get_citationindex(browser)

    # the button links are the only ones with 'div' tags inside
    links = [x for x in soup.find_all('a') if x.find('div')]
    talks = [x for x in links if "getTalk" in x.get('onclick')]
    header = soup.find(class_='volumetitle')

    if talks:
        # if talks are found, then return the data
        for k in talks:
            ref = k.find(class_='reference').text
            title = k.find(class_='talktitle').text
            print(script, header.text, ref, title)
    else:
        # if no talks are found yet, keep digging down (recursive call)
        for k in links:
            script = k.get('onclick')
            browser.execute_script(script)
            time.sleep(1)
            dig_into_citations(browser, script)


# Open Chrome to the start page (the latest driver for Chrome 87 is sitting in the project folder)
browser = webdriver.Chrome()
browser.implicitly_wait(20)
#browser.get('https://scriptures.byu.edu/#::fNYNY7267e4010d6')
dig_into_citations(browser)
