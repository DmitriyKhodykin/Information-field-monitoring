# Module for uploading RIA news feeds to a local database
# Python 3.7. PEP8
# pip install lxml

# Imports
import requests
from bs4 import BeautifulSoup as Bs

# Resources
url = 'https://www.ria.ru'


def ria_parser_refs():
    """Returns a list of news page addresses (ref's)"""

    source = requests.get(url).text
    soup = Bs(source, 'lxml').find('span', class_='share')
    refs = []
    raw_result = soup.find_all_next('a', href=True)

    for ref in raw_result:
        if 'html' in ref.get('href') and 'http' in ref.get('href'):
            refs.append(ref.get('href'))

    return refs


def ria_parser_body(ref):
    """Returns 3 thousand characters of the text of the news
    in response to its address"""

    result = str()

    source = requests.get(ref).text
    soup = Bs(source, 'lxml')
    raw_result = soup.find_all('div', class_='article__text')

    for i in raw_result:
        result = result + i.text + ' '

    return result[:3000]
