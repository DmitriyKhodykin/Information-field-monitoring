# Module for uploading INTERFAX news feeds to a local database
# Python 3.7. PEP8
# pip install lxml

# Imports
import requests
from bs4 import BeautifulSoup as Bs
import re

# Resources
url = 'https://www.interfax.ru'


def interfax_parser_refs():
    """Returns a list of news page addresses (ref's)"""

    source = requests.get(url).text
    soup = Bs(source, 'lxml').find('main')
    refs = []
    raw_result = soup.find_all_next('a', href=True)

    for ref in raw_result:
        if re.search('[0-9]', ref.get('href')) and all(
                elm not in ref.get('href') for elm in [
                    'http', 'photo', 'html', 'story', 'pressreleases', 'asp', 'aeroflot'
                ]
        ):
            refs.append(ref.get('href'))

    return refs


def interfax_parser_body(ref):
    """Returns 4 thousand characters of the text of the news"""

    result = str()

    source = requests.get(f'{url}{ref}')
    source.encoding = 'cp1251'
    source = source.text
    soup = Bs(source, 'lxml').find('div', class_='mainblock')
    raw_result = soup.find_all_next('p')

    for i in raw_result:
        if len(i.text) > 0:
            result = result + i.text + ' '

    return result[:4000]
