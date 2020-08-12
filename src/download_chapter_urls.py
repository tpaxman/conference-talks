import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd

volumes_url = 'https://scriptures.byu.edu/#::fNYNY7267e401'
browser = webdriver.Chrome()
browser.implicitly_wait(5)

df_books = pd.read_csv('output/book_urls.csv')
chaps_data = []

for b in df_books.book_url:
    # browse_to(browser, b)
    browser.get(b)
    time.sleep(1)
    # browse_to(browser, b)
    try:
        browser.find_element_by_class_name('chaptersblock')
        soup = BeautifulSoup(browser.page_source)
        chapblock = soup.find(class_='chaptersblock')
        chaps = chapblock.find_all('a')
        # print(len(chaps), b)
        for c in chaps:
            book_num, chap_num = re.findall(r'.*Filter\(\'(\d+)\', \'(\d+).*', c.attrs['onclick'])[0]
            chaps_data.append((int(book_num), int(chap_num)))
            print(book_num, chap_num)
    except:
        # some books don't have chapters (goes directly to the verses list) like Jarom, Omni, etc.
        # flagged here by assigning None to chap_num
        book_num = df_books.set_index('book_url').loc[b, 'book_num']
        chap_num = 1
        chaps_data.append((book_num, chap_num))
        print(book_num, chap_num)

df_chaps = pd.DataFrame(chaps_data, columns=['book_num', 'chap_num'])
df_chapcounts = df_chaps.groupby('book_num').count().reset_index().rename(columns={'chap_num': 'chap_count'})
df_chaps = df_chaps.merge(df_chapcounts, on='book_num')
df_chaps['chap_category'] = df_chaps.chap_count.apply(lambda x: 'single' if x == 1 else 'multiple')
df_chaps = df_chaps.merge(df_books, on='book_num')


def get_chap_url(book_url, chap_num, chap_category):
    if chap_category == 'multiple':
        hexnum = hex(chap_num)[2:].zfill(2)
        return f'{book_url}{hexnum}'
    elif chap_category == 'single':
        return f'{book_url}'

df_chaps['chap_url'] = df_chaps.apply(lambda r: get_chap_url(r.book_url, r.chap_num, r.chap_category), axis=1)


df_chaps.to_csv('output/chapter_urls.csv', index=False)