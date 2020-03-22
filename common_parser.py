# Module for parsing all sites
# Python 3.7. PEP8
# pip install lxml

# Import Library
import requests
from bs4 import BeautifulSoup as Bs
import re
import time


class Parser:

    def __init__(self, url):
        self.url = url

    def get_parser_refs(self):
        """Returns a list of news page addresses"""

        source = requests.get(self.url).text

        # Create soup object
        if "ria" in self.url:
            soup = Bs(source, 'lxml').find('span', class_='share')
        elif "tass" in self.url:
            soup = Bs(source, 'lxml').find('main', class_='container')
        elif "interfax" in self.url:
            soup = Bs(source, 'lxml').find('main')
        else:
            pass

        refs = []
        raw_result = soup.find_all_next('a', href=True)

        # Get List of all refs
        if "ria" in self.url:
            for ref in raw_result:
                if all(elm in ref.get('href') for elm in ['html', 'http']):
                    refs.append(ref.get('href'))

        elif "tass" in self.url:
            for ref in raw_result:
                if re.search('[0-9]', ref.get('href')) and all(elm not in ref.get('href') for elm in ['http', 'press']):
                    refs.append(ref.get('href'))

        elif "interfax" in self.url:
            for ref in raw_result:
                if re.search('[0-9]', ref.get('href')) and all(
                        elm not in ref.get('href') for elm in [
                            'http', 'photo', 'html', 'story', 'pressreleases', 'asp', 'aeroflot'
                        ]):
                    refs.append(ref.get('href'))

        else:
            pass

        return refs

    def get_parser_body(self, ref):
        """Returns 4 thousand characters of the text of the news in response"""

        result = str()

        if "ria" in self.url:
            source = requests.get(ref).text
            soup = Bs(source, 'lxml')
            raw_result = soup.find_all('div', class_='article__text')

            for i in raw_result:
                result = result + i.text + ' '

        elif "interfax" in self.url:
            source = requests.get(f'{self.url}{ref}')
            source.encoding = 'cp1251'
            source = source.text
            soup = Bs(source, 'lxml').find('div', class_='mainblock')
            raw_result = soup.find_all_next('p')

            for i in raw_result:
                result = result + i.text + ' '

        elif "tass" in self.url:
            source = requests.get(f'{self.url}{ref}').text
            soup = Bs(source, 'lxml')
            raw_result = soup.find_all('div', class_='text-content')
            result = result + raw_result[0].text

        else:
            pass

        return result[:4000]


if __name__ == "__main__":

    def test():
        urls = [
            'https://www.ria.ru',
            'https://www.interfax.ru',
            'https://tass.ru'
                ]
        nn = 0

        for url in urls:
            parser = Parser(url)
            refs = parser.get_parser_refs()
            for ref in refs:
                print(
                    nn,
                    ref,
                    parser.get_parser_body(ref)
                )
                time.sleep(1)
                nn = nn + 1

    test()
