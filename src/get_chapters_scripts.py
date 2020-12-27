from selenium import webdriver
import time
from citationindex import get_citationindex_dynamic
import sys

books_scripts_file, base_url, output_file = sys.argv[1:]

def main():
    # Open Chrome to the start page (the latest driver for Chrome 87 is sitting in the project folder)
    browser = webdriver.Chrome()
    browser.implicitly_wait(20)
    browser.get(base_url)
    time.sleep(5)

    with open(books_scripts_file, encoding='utf-8') as f:
        book_scripts = [x for x in f.read().split('\n') if x]

    with open(output_file, 'w', encoding='utf-8') as f:
        for x in book_scripts:
            browser.execute_script(x)
            time.sleep(1)
            soup = get_citationindex_dynamic(browser)
            chapter_scripts = [x.get('onclick') for x in soup.find_all('a') if x.find('div')]

            for y in chapter_scripts:
                f.write(f'{y}\n')

if __name__ == '__main__':
    main()


