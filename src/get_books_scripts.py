from selenium import webdriver
import time
from citationindex import get_citationindex_dynamic
import sys

output_file, volumes_url = sys.argv[1:]

def main():
    # Open Chrome to the start page (the latest driver for Chrome 87 is sitting in the project folder)
    browser = webdriver.Chrome()
    browser.implicitly_wait(20)
    browser.get(volumes_url)
    time.sleep(5)

    soup = get_citationindex_dynamic(browser)
    scripts = [x.get('onclick') for x in soup.find_all('a') if x.find('div')]

    with open(output_file, 'w', encoding='utf-8') as f:
        for x in scripts:
            f.write(f'{x}\n')

if __name__ == '__main__':
    main()


