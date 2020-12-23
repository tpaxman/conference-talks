from pathlib import Path
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

VOLUMES_URL = 'https://scriptures.byu.edu/#::fNYNY7267e410'
output_folder = Path('page_sources_citfreq')

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

browser = webdriver.Chrome()
browser.implicitly_wait(20)
browser.get(VOLUMES_URL)
time.sleep(4)
soup = get_citationindex(browser)
topscrips = [x for x in soup.find_all('a') if x.find('div')]

for k in topscrips:
    script = k.get('onclick')
    browser.execute_script(script)
    time.sleep(1)
    soup = get_citationindex(browser)
    filestem = '_'.join(re.findall(r"\'(.*?)\'", script))
    filename = filestem + '.html'
    filepath = output_folder / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
