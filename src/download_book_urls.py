import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd

browser = webdriver.Chrome()
books_url = 'https://scriptures.byu.edu/#::fNYNY7267e401'
browser.implicitly_wait(20)
browser.get(books_url)
voltitles = BeautifulSoup(browser.page_source).find_all(class_='volumetitle')
volsoup = BeautifulSoup(browser.page_source).find_all(class_='volumecontents')
volumes = dict(zip([x.text.strip() for x in voltitles], volsoup))

volumes_data = []
for vol_name, vol_tag in volumes.items():
    book_tags_list = vol_tag.find_all('a')
    for book_tag in book_tags_list:
        book_num = int(re.sub(r'.*book=(\d+).*', r'\1', book_tag.get_attribute_list('onclick')[0]))
        book_name = book_tag.text
        volumes_data.append((vol_name, book_name, book_num))

df = pd.DataFrame(volumes_data, columns=('volume', 'book_name', 'book_num'))

def get_book_url(book_num):
    hexnum = hex(book_num)[2:].zfill(3)
    return f'{books_url}{hexnum}'

df['book_url'] = df.book_num.apply(get_book_url)


df.to_csv('output/book_urls.csv', index=False)


#
# browser.get(df.book_url[0])
# time.sleep(5)
# browser.get(df.book_url[0])
# html_source = browser.page_source
# chaps = BeautifulSoup(html_source).find(class_='chaptersblock')
#
#
# try:
#     element = WebDriverWait(browser, 20).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'chaptersblock'))
#     )
# finally:
#     html_source = browser.page_source
#
#
# chaps = BeautifulSoup(browser.page_source).find(class_='chaptersblock')
# re.findall(r'.*Filter\(\'(\d+)\', \'(\d+).*', chaps.find_all('a')[0].attrs['onclick'])[0]
