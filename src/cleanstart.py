from selenium import webdriver
import time

WebElement = webdriver.remote.webelement.WebElement


def main():
    base_url = 'https://scriptures.byu.edu/#::fNYNY7267e413'
    browser = webdriver.Chrome()
    browser.get(base_url)
    browser.implicitly_wait(5)
    root_button_elems = find_button_elems(browser)

    d = get_buttons_details_dict(root_button_elems)

    old_button_elems = root_button_elems
    dd = {}
    for title, script in d.items():
        browser.execute_script(script)
        print(f'execute {script} ({title})')
        new_button_elems = find_button_elems_wait_wrapper(browser, old_button_elems)
        d2 = get_buttons_details_dict(new_button_elems)
        old_button_elems = new_button_elems
        dd[title] = d2


def get_buttons_details_dict(button_elems : list) -> dict:
    d = {}
    for button_elem in button_elems:
        link_elem = extract_link_tag_from_button(button_elem)
        script = extract_script_from_link(link_elem)
        title = extract_button_title_from_link(link_elem)
        d[title] = script
        print("get details for", title, script)
    return d


def check_that_page_has_changed(new_button_elements, old_button_elements):
    def extract_buttons_text(button_elements):
        return ''.join([x.text for x in button_elements])

    return extract_buttons_text(new_button_elements) == extract_buttons_text(old_button_elements)


def find_button_elems_wait_wrapper(browser, old_button_elements):
    new_button_elements = find_button_elems(browser)
    if check_that_page_has_changed(new_button_elements, old_button_elements):
        return new_button_elements
    else:
        time.sleep(3)
        return find_button_elems(browser)


def find_button_elems(browser):
    button_elements = (browser
                       .find_element_by_class_name('sciwrapper')
                       .find_element_by_class_name('scicontent')
                       .find_element_by_class_name('nano-content')
                       .find_elements_by_tag_name('li'))
    return button_elements


def extract_link_tag_from_button(button_elem: WebElement) -> WebElement:
    assert button_elem.tag_name == 'li', 'button_elem must be an "li" tag'
    link_tag = button_elem.find_element_by_tag_name('a')
    assert link_tag, f"no link was found in {button_elem}"
    return link_tag


def extract_button_title_from_link(link_elem: WebElement) -> str:
    raw_button_text = link_elem.text
    lines_of_text = raw_button_text.count('\n') + 1
    assert lines_of_text == 2, f"expected button text to have 2 lines but text is {raw_button_text}"
    button_text_pieces = raw_button_text.split('\n')
    title = button_text_pieces[0]
    return title


def extract_script_from_link(link_tag: WebElement) -> str:
    assert link_tag.tag_name == 'a', "link_tag must be an 'a' element"
    assert 'onclick' in get_element_attributes(link_tag), "link_tag must have 'onclick' attribute"
    script = link_tag.get_attribute('onclick')
    return script


# GENERAL HELPERS

def get_element_attributes(elem: webdriver.remote.webelement.WebElement) -> dict:
    list_of_dicts_of_attributes_properties = elem.get_property('attributes')
    attributes_dict = {x['nodeName']: x['nodeValue'] for x in list_of_dicts_of_attributes_properties}
    return attributes_dict


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
