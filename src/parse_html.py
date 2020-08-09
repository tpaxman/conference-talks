from bs4 import BeautifulSoup
import requests
import re

def getit(talknum):
    filename = f'data/talk_{talknum}.html'
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html)

    talklabel = soup.find('div', id='talklabel')
    details = re.findall(r'(\d+)–(\w):\d+,\s+(.*),\s+(.*)$', talklabel.text)[0]
    year = int(details[0])
    month = details[1]
    speaker = details[2]
    title = details[3]

    talktext = soup.find('div', id='centercolumn')

    if talknum < 2000:
        calling = talktext.find(class_='gcspkpos').text.strip()
        bodyhtml = talktext.find(class_='gcbody')
        citations = [x.text.strip() for x in bodyhtml.find_all(class_='citation')]
    else:
        byline = [x.text for x in talktext.find(class_='byline').find_all('p')]
        calling = byline[1]
        bodyhtml = talktext.find(id='primary')
        citations = [x.text.strip() for x in bodyhtml.find_all(class_='citation')]

    print('\n'.join([title, speaker, calling, str(year), month, '\n'.join(citations)]))


def checksave(hexnum):
    a = requests.get(f'https://scriptures.byu.edu/#:t{hexnum}')
    with open(f'data/test_{hexnum}.html', 'w', encoding='utf-8') as f:
        f.write(a.text)



for x in range(1,20):
    getit(x)


# from bs4 import BeautifulSoup
#
# url = "http://legendas.tv/busca/walking%20dead%20s03e02"
# browser = webdriver.PhantomJS()
# browser.get(url)
# html = browser.page_source
# soup = BeautifulSoup(html, 'lxml')
# a = soup.find('section', 'wrapper')
#
#
# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get("https://www.nytimes.com")
# headlines = driver.find_elements_by_class_name("story-heading")
# for headline in headlines:
#     print(headline.text.strip())