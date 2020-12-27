from bs4 import BeautifulSoup

def get_citationindex(page_source):
    """
    Finds the location of the citationindex button links (either in citationindex or citationindex2)
    The links will be in either 'citationindex' or 'citationindex2' but it is not clear which will be the correct one
    Gets the HTML associated with both citation index elements and attempts to find links inside
    """
    citation_id_names = ['citationindex', 'citationindex2']
    citation_id_soups = [BeautifulSoup(page_source, features='lxml').find(id=x) for x in citation_id_names]
    soup_list = [soup for soup in citation_id_soups if soup.find_all('a')]
    if soup_list:
        citationindex_soup = soup_list[0]
        return citationindex_soup
    else:
        return None

def get_citationindex_dynamic(browser):
    """
    Gets the name of the citationindex element that contains the links of interest.
    This script waits until they both load and finds the one that has the links in it and returns a bs4 Soup object.
    """
    # This runs until the page has actually loaded and the links are found inside the proper citationindex element
    citationindex_soup = None
    while not citationindex_soup:
        citationindex_soup = get_citationindex(page_source=browser.page_source)
    return citationindex_soup