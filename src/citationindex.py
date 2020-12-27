from bs4 import BeautifulSoup


def get_citationindex(browser):
    """
    Gets the name of the citationindex element that contains the links of interest.
    The links will be in either 'citationindex' or 'citationindex2' but it is not clear which will be the correct one
    This script waits until they both load and finds the one that has the links in it and returns a bs4 Soup object.
    """

    # This runs until the page has actually loaded and the links are found inside the proper citationindex element
    soup_list = []
    while not soup_list:
        soup_list = get_soup_list(browser)

    # the BeautifulSoup object of the citation index element is returned (i.e. for 'citationindex' or 'citationindex2')
    citationindex_soup = soup_list[0]
    return citationindex_soup


def get_soup_list(browser):
    """Gets the HTML associated with both citation index elements and attempts to find links inside"""
    citation_id_names = ['citationindex', 'citationindex2']
    page_source = browser.page_source
    citation_id_soups = [BeautifulSoup(page_source, features='lxml').find(id=x) for x in citation_id_names]
    soup_list = [soup for soup in citation_id_soups if soup.find_all('a')]
    return soup_list
