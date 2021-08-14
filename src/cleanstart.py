from selenium import webdriver

def main():
    base_url = 'https://scriptures.byu.edu/#::fNYNY7267e413'
    browser = webdriver.Chrome()
    browser.get(base_url)
    browser.implicitly_wait(5)
    start_elems = find_elems_of_interest(browser)

    for x, y in start_elems:
        print(y)
        browser.execute_script(y)
        elems = find_elems_of_interest(browser)
        print(elems)
        recur(browser, x, y)


def recur(browser, text, script):
    print(script)
    browser.execute_script(script)
    browser.implicitly_wait(2)
    elems = find_elems_of_interest(browser)
    for x, y in elems:
        if 'getFilter' in y:
            recur(browser, x, y)
        elif 'getTalk' in y:
            print(text, x, y)


def find_elems_of_interest(browser):
    yes = [(x, x.get_attribute('onclick')) for x in browser.find_elements_by_tag_name('a')]
    no = [x.get_attribute('onclick') for x in browser.find_element_by_id('scicrumb').find_elements_by_tag_name('a')]
    yay = [(x.text, y) for x, y in yes if y and (y not in no) and (('getFilter' in y) or ('getTalk' in y)) and x]
    mmm = [x for x in yay if x[0]]
    return mmm

if __name__ == '__main__':
    main()

    # rawelems = {x.text: x.get_attribute('onclick') for x in browser.find_elements_by_tag_name('a')}
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

[x.get_attribute('onclick') for x in browser.find_element_by_class_name('chaptersblock').find_elements_by_tag_name('a')]



#
# elems = [x for x in browser.find_elements_by_tag_name('a') if x.get_attribute('onclick') and ('getFilter' in x.get_attribute('onclick'))]