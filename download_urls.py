from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import time

ROOT_URL = 'https://scriptures.byu.edu/#::fNYNY7267e401'

def get_book_url(book_num):
    book_hexnum = hex(book_num)[2:].zfill(3)
    return ROOT_URL + book_hexnum

def get_chapter_url(book_num, chapter_num):
    book_url = get_book_url(book_num)
    chapter_hexnum = hex(chapter_num)[2:].zfill(2)
    return book_url + chapter_hexnum

def get_verse_url(book_num, chapter_num, verse_num):
    chapter_url = get_chapter_url(book_num, chapter_num)
    return chapter_url + str(verse_num)

def get_book_nums(browser):
    browser.implicitly_wait(20)
    browser.get(ROOT_URL)
    browser.find_element_by_id('scriptures2')
    # time.sleep(5)
    soup = BeautifulSoup(browser.page_source)
    citations = soup.find(id='scriptures2')
    voltitles = citations.find_all(class_='volumetitle')
    volsoup = citations.find_all(class_='volumecontents')
    volumes = dict(zip([x.text.strip() for x in voltitles], volsoup))
    volumes_nums = {}
    for vol_name, vol_tag in volumes.items():
        book_tags_list = vol_tag.find_all('a')
        for book_tag in book_tags_list:
            book_num_string = book_tag.attrs['onclick']
            # print(book_num_string)
            # book_num = int(re.sub(r'.*Filter\(\'(\d+)\'.*', r'\1', book_num_string))
            book_num = int(re.sub(r'.*book=(\d+).*', r'\1', book_num_string))
            book_name = book_tag.text
            volumes_nums[book_num] = book_name
    return volumes_nums

def get_chapter_nums(browser, book_num):
    book_url = get_book_url(book_num)
    browser.implicitly_wait(5)
    browser.get(book_url)
    time.sleep(1)
    chaps_data = []
    try:
        browser.find_element_by_class_name('chaptersblock')
        soup = BeautifulSoup(browser.page_source)
        chapblock = soup.find(class_='chaptersblock')
        chaps = chapblock.find_all('a')
        print(len(chaps), book_url)
        for c in chaps:
            chapter_num_string = c.attrs['onclick']
            chapter_num = int(re.sub(r'.*Filter\(\'\d+\', \'(\d+).*', r'\1', chapter_num_string))
            chaps_data.append(chapter_num)
    except:
        # some books don't have chapters (goes directly to the verses list) like Jarom, Omni, etc.
        chapter_num = 1
        chaps_data.append(chapter_num)

    return chaps_data


def get_verse_nums(browser, book_num, chapter_num):
    chapter_url = get_chapter_url(book_num, chapter_num)
    browser.implicitly_wait(30)

    browser.get(chapter_url)
    browser.refresh()
    # time.sleep(4)
    verses_data = []
    browser.find_element_by_id('citationindex2')
    # browser.find_element_by_class_name('referencesblock')
    browser.find_element_by_class_name('citationcount')
    soup = BeautifulSoup(browser.page_source)
    verseblock = soup.find(id='citationindex2').find(class_='referencesblock')
    verses = verseblock.find_all('a')
    for v in verses:
        verse_num_string = v.attrs['onclick']
        print(verse_num_string)
        verse_num = int(re.sub(r'getFilter.*\'\d+\',.*\'\d+\',.*\'(\d+)\'.*', r'\1', verse_num_string))
        print(verse_num)
        verses_data.append(verse_num)

    unique_verses = list(set(verses_data))
    return unique_verses





# browser = webdriver.Chrome()
# get_book_nums(browser)
# get_chapter_nums(browser, 110)
get_verse_nums(browser, 101, 5)