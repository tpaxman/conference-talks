from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

WebElement = webdriver.remote.webelement.WebElement


def main():
    base_url = 'https://scriptures.byu.edu/#::fNYNY7267e413'
    browser = webdriver.Chrome()
    parent_details = ''
    with open('talks_output.txt', 'w') as f:
        the_machine(browser, base_url, parent_details, f)


def the_machine(browser, url, parent_details, file_to_write):
    browser.get(url)
    try:
        button_elems = find_button_elems(browser)
    except:
        # this handles cases like "headnote" buttons which open nothing
        print(f'skipping {parent_details}')
        return
    for button_elem in button_elems:
        link_elem = extract_link_tag_from_button(button_elem)
        script = extract_script_from_link(link_elem)
        if 'getTalk' in script:
            link_elem = extract_link_tag_from_button(button_elem)
            reference = extract_talk_reference(link_elem)
            title = extract_talk_title(link_elem)
            file_to_write.write(parent_details + ' ; ' + url + ' ; ' + reference + ' ; ' + title + '\n')
            print('------', reference.replace('\n', '___'), title.replace('\n', '___'))
        else:
            title = extract_button_title_from_link(link_elem)
            if '(JST)' in title:
                # JST button links also appear to do nothing
                print(f'skipping {title}')
                continue
            else:
                print('execute: ' + script + ', ' + title)
                browser.execute_script(script)
                # this seems to be required to avoid "stale element" errors:
                new_url = browser.current_url
                the_machine(browser, new_url, parent_details + ' ; ' + title, file_to_write)


def extract_talk_reference(link_elem: BeautifulSoup) -> str:
    return link_elem.find(class_='reference').text


def extract_talk_title(link_elem: BeautifulSoup) -> str:
    return link_elem.find(class_='talktitle').text


def find_button_elems(browser):
    sciwrapper = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sciwrapper")))
    soup = BeautifulSoup(sciwrapper.get_attribute('outerHTML'), 'html.parser')
    button_elements = soup.find(class_='scicontent').find(class_='nano-content').find_all('li')
    return button_elements


def extract_link_tag_from_button(button_elem: BeautifulSoup) -> BeautifulSoup:
    assert button_elem.name == 'li', 'button_elem must be an "li" tag'
    link_tag = button_elem.find('a')
    assert link_tag, f"no link was found in {button_elem}"
    return link_tag


def extract_button_title_from_link(link_elem: BeautifulSoup) -> str:
    text_tags = link_elem.find_all('div')
    list_without_citationcount = [x for x in text_tags if ('citationcount' not in x.get('class'))]
    assert len(
        list_without_citationcount) == 1, f'got more text tags than expected in {[x.text for x in list_without_citationcount]}'
    title = list_without_citationcount[0].text
    return title


def extract_script_from_link(link_tag: BeautifulSoup) -> str:
    assert link_tag.name == 'a', "link_tag must be an 'a' element"
    assert 'onclick' in link_tag.attrs, "link_tag must have 'onclick' attribute"
    script = link_tag.get('onclick')
    return script


# MAIN SCRIPT

if __name__ == '__main__':
    main()

# JUNK

# def recur(browser, text, script):
#     print(script)
#     browser.execute_script(script)
#     browser.implicitly_wait(2)
#     elems = find_button_elems(browser)
#     for x, y in elems:
#         if 'getFilter' in y:
#             recur(browser, x, y)
#         elif 'getTalk' in y:
#             print(text, x, y)
#
#
#
#     # rawelems = {x.text: x.get_attribute('onclick') for x in browser.find_elements_by_tag_name('a')}
# nopes = [x.get_attribute('onclick') for x in browser.find_element_by_id('scicrumb').find_elements_by_tag_name('a')]
# elems = {t: s for t, s in rawelems.items() if s and (s not in nopes) and 'getFilter' in s}

# getfilt = [y for x, y in yay if ('getFilter' in y)]
# gettalk = [y for x, y in yay if ('getTalk' in y)]


# yes = [x for x in browser.find_elements_by_tag_name('a') if x.get_attribute('onclick')]
# no = [x for x in browser.find_element_by_id('scicrumb').find_elements_by_tag_name('a')]
# yay = [x.get_attribute('onclick') for x in yes if 'getFilter' in x.get_attribute('onclick') and x not in no]

# THEFUN(script)
# run script
# collect all 'a' tags
# get text, script from a-tags
# check that scripts are getFilter or getTalk
# for each where script = getTalk
#    save text, script, parent-script
# for each where script = getFilter
#    THEFUN(script)


# Volumes - volumecontents -getFilter (multiple blocks)
# Chapters - chaptersblock - getFilter
# Verses - referencesblock - getFilter
# Talks - referencesblock - getTalk


#
# elems = [x for x in browser.find_elements_by_tag_name('a') if x.get_attribute('onclick') and ('getFilter' in x.get_attribute('onclick'))]
