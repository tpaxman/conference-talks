import re
from selenium import webdriver
import time
from citationindex import get_citationindex_dynamic
import sys

# chapters_scripts_file, base_url, output_file = sys.argv[1:]

base_url = 'https://scriptures.byu.edu/#::fNYNY7267e413'
chapters_file = 'output/chapter-scripts.txt'
verses_file = 'output/verses-scripts.txt'
output_folder = 'output/references-pagesources'

def get_getfilter_args(script: str) -> list:
    return re.findall(r"\'(.*?)\'", script)

def main():

    with open(chapters_file) as f:
        chaps = f.read()

    with open(verses_file) as f:
        verses = f.read()

    final_scripts = sorted([x for x in (chaps + verses).split('\n')
                            if (len(get_getfilter_args(x)) == 4)
                            & ('getFilter' in x)
                            & ('JST' not in x)])

    # Open Chrome to the start page (the latest driver for Chrome 87 is sitting in the project folder)
    browser = webdriver.Chrome()
    browser.implicitly_wait(20)
    browser.get(base_url)
    time.sleep(5)
    for x in final_scripts:
        browser.execute_script(x)
        time.sleep(1)
        soup = get_citationindex_dynamic(browser)
        print(x,' ',soup.find('div', class_='volumetitle').text)
        filename = '_'.join(get_getfilter_args(x)) + '.html'
        with open(output_folder + '/' + filename, 'w') as f:
            f.write(str(soup))

if __name__ == '__main__':
    main()
