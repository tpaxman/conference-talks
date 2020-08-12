from bs4 import BeautifulSoup
import re
import json

def main():
    for x in range(1, 8460):
        if x not in range(1825, 2000):
            citation_data = get_citation_data(x)
            save_citation_data(citation_data)
            print(f'saved {x}')

def get_citation_data(talknum):
    # read html file
    soup = import_html_file(talknum)

    # get talk details
    labeltxt = soup.find('div', id='talklabel').text
    year, month, speaker, title = re.findall(r'(\d+)–(\w):\d+,\s+(.*),\s+(.*)$', labeltxt)[0]

    # get citations from body
    talktext = soup.find('div', id='centercolumn')
    if talknum < 2000:
        bodyhtml = talktext.find(class_='gcbody')
    elif 2000 <= talknum < 8362:
        bodyhtml = talktext.find(id='primary')
    elif talknum >= 8362:
        bodyhtml = talktext.find(class_='body-block')
    footnotes_html = [str(x) for x in bodyhtml.find_all(class_='footnote')]
    # citations = [unicodedata.normalize('NFKD', x.text.strip())
    #              for x in bodyhtml.find_all(class_='citation')]

    return {'talknum': talknum,
            'year': int(year),
            'month': month,
            'speaker': speaker,
            'title': title,
            'footnotes_html': footnotes_html}

def import_html_file(talknum):
    filename = f'data/talk_{talknum}.html'
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, features='html.parser')
    return soup


def save_citation_data(citation_data):
    talknum = citation_data['talknum']
    with open(f'data/talk_{talknum}.json', 'w', encoding='utf-8') as f:
        json.dump(citation_data, f)




if __name__=='__main__':
    main()

# def checksave(hexnum):
#     a = requests.get(f'https://scriptures.byu.edu/#:t{hexnum}')
#     with open(f'data/test_{hexnum}.html', 'w', encoding='utf-8') as f:
#         f.write(a.text)


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