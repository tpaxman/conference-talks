from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

ROOT_URL = 'https://scriptures.byu.edu/#::fNYNY7267e401'


def main():
    df = pd.concat([pd.read_csv(x) for x in Path('data2').glob('*.csv')])
    df = df.drop(columns='Unnamed: 0')
    # df['verse_url'] = df.apply(lambda r: get_verse_url(r.book, r.chapter, r.verse), axis=1)
    # df['filename'] = df.book + '_' + df.chapter + '_' + df.verse + '.html'
    browser = webdriver.Chrome()
    df.apply(lambda r: get_verse_citations(browser, r.book, r.chapter, r.verse), axis=1)
    for i, r in df.iterrows():
        soup = get_verse_citations(browser, r.book, r.chapter, r.verse)
        print(r.book, r.chapter, r.verse)
        filename = f'{r.book}_{r.chapter}_{r.verse}.html'
        with open(f'data5/{filename}', 'w', encoding='utf-8') as f:
            f.write(str(soup))


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


def get_verse_citations(browser, book, chapter, verse):
    verse_url = get_verse_url(book, chapter, verse)
    browser.implicitly_wait(30)
    browser.get(verse_url)
    browser.refresh()
    browser.find_element_by_id('citationindex2')

    soup = BeautifulSoup(browser.page_source)
    # goodstuff = soup.find(id='citationindex2').find(class_='referencesblock')
    return soup
    # filename = f'{book}_{chapter}_{verse}.html'
    # with open(f'data5/{filename}', 'w', encoding='utf-8') as f:
    #     f.write(str(soup))
    # print(filename)


if __name__ == '__main__':
    main()
