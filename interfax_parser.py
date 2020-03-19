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
        if re.search('[0-9]', ref.get('href')) \
                and 'http' not in ref.get('href') \
                and 'photo' not in ref.get('href') \
                and 'html' not in ref.get('href') \
                and 'story' not in ref.get('href') \
                and 'pressreleases' not in ref.get('href'):
            refs.append(ref.get('href'))

    return refs


