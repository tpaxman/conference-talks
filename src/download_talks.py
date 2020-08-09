
"""
- Talks are numbered with hexadecimal from 1 (April 1942) to 210b (April 2020)

- Format is `https://scriptures.byu.edu/#:t<talknumber>`

## Citations:
- <span class="citation" id="130466"><a href="javascript:void(0)" onclick="sx(this, 130466)">&nbsp;</a><a href="javascript:void(0)" onclick="gs(130466)">1&nbsp;Corinthians 11:11</a></span>

## Talk Details:
- found in div, id='talklabel'
- string content: "<year>-<month-initial>:<talknumber>, <speaker_name>, <title>"
<div id="talklabel" class="visiblelabel"><a href="javascript:void(0);" onclick="getConf('2015', 'A');">2015–A</a>:14, Bonnie L. Oscarson, Defenders of the Family Proclamation</div>


```
```
"""
import time
import requests
from selenium import webdriver
import argparse

START = 1
END = 8459

def main():
    parser = argparse.ArgumentParser(description='Get talk number to read')
    parser.add_argument('start_talknum', type=int, help='the number of the talk to start with')
    parser.add_argument('--upto', type=int, default=None, help='the number of the talk to end with')
    args = parser.parse_args()

    browser = webdriver.Chrome()

    start = args.start_talknum
    end = args.upto

    if not end:
        end = start

    for talknum in range(start, end + 1):
        download_talk(browser, talknum)


def download_talk(browser, talknum):
    hexnum = hex(talknum)[2:]
    url = f'https://scriptures.byu.edu/#:t{hexnum}>'
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    filename = f'data/talk_{talknum}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'downloaded {filename}')


if __name__=='__main__':
    main()