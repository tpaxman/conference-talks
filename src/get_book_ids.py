"""
Download Book URLs

- Creates a table of all scripture index urls for each book of scripture.
- Output is a CSV of 94 books of scripture with columns 'volume, book_name, book_num, book_url'
- Algorithm description:
  - Navigates to 'https://scriptures.byu.edu/#::fNYNY7267e401'
  - Locates the source html associated with the "Scriptures" pane on the left
  - Gets the 5 volume names (Old Testament, New Testament, etc.)
  - Gets the names of each book and their IDs
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import sys

VOLUMES_URL = 'https://scriptures.byu.edu/#::fNYNY7267e401'


def main():
    # get output filename from command line
    output_file = sys.argv[1]

    # open Chrome webdriver (the latest driver for Chrome 87 is sitting in the project folder)
    browser = webdriver.Chrome()

    # configure browser to wait for stuff to load
    browser.implicitly_wait(20)

    # Locate the scripture pane on the left side of the page
    browser.get(VOLUMES_URL)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, features="lxml")
    scripture_pane = soup.find_all(class_='scripturewrapper')[0]

    # Get the titles of each of the 5 volumes
    volnames = [x.text.strip() for x in scripture_pane.find_all(class_='volumetitle')]
    # Get the Book titles and their corresponding links for each of the 5 volumes
    books_tags = [x.find_all('a') for x in scripture_pane.find_all(class_='volumecontents')]

    # save the volume names with the books they contain as a table
    book_ids = [{y.text: get_book_id(y) for y in x} for x in books_tags]
    df = pd.DataFrame([(vol, book, booknum)
                       for vol, booksdict in zip(volnames, book_ids)
                       for book, booknum in booksdict.items()],
                      columns=['volume', 'book_name', 'book_id'])
    df.to_csv(output_file, index=False)


def get_book_id(souptag):
    """
    This gets the id number of a scripture book from a link tag (i.e. <a href...> soup tag)
    Each of the book tag links looks like this:
    <a href="javascript:void(0);" onclick="getScripture('?book=405&amp;chapter=&amp;verses=&amp;jst=')">JS—History</a>,
    """
    onclick_contents = souptag.get_attribute_list('onclick')[0]
    book_num_string = re.sub(r'.*book=(\d+).*', r'\1', onclick_contents)
    book_num = int(book_num_string)
    return book_num


if __name__ == '__main__':
    main()
