# Module for uploading TASS news feed to a local database
# Python 3.7. PEP8
# pip install lxml
# request limit 3 sec

# Imports
import requests
from bs4 import BeautifulSoup as Bs
import re

# Resources
url = 'https://tass.ru'


def tass_parser_refs():
    """Returns a list of news page addresses (ref's)"""

    source = requests.get(url).text
    soup = Bs(source, 'lxml').find('main', class_='container')
    refs = []
    raw_result = soup.find_all_next('a', href=True)

    for ref in raw_result:
        if re.search('[0-9]', ref.get('href')) \
                and 'http' not in ref.get('href') \
                and 'press' not in ref.get('href'):
            refs.append(ref.get('href'))

    return refs


def tass_parser_body(ref):
    """Returns 3 thousand characters of the text of the news in response
    to its address https://tass.ru/ref (example, '/politika/7999199')"""

    source = requests.get(f'{url}{ref}').text
    soup = Bs(source, 'lxml')
    raw_result = soup.find_all('div', class_='text-content')
    result = raw_result[0].text[:3000]

    return result
