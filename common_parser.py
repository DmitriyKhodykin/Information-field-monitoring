# Module for parsing all sites
# Python 3.7. PEP8
# pip install lxml

# Import Library
import requests
from bs4 import BeautifulSoup as Bs
import re

class Parser:


    def __init__(self, url):
        self.url = url
    

    def get_parser_refs(self):
        """Returns a list of news page addresses"""

        source = requests.get(self.url).text

        #Create soup object
        if("ria" in self.url):
            soup = Bs(source, 'lxml').find('span', class_='share')
        elif("tass" in self.url):
            soup = Bs(source, 'lxml').find('main', class_='container')
        elif("interfax" in self.url):
            soup = Bs(source, 'lxml').find('main')
        else:
            pass   

        refs = []
        raw_result = soup.find_all_next('a', href=True)

        #Get List of all refs
        if("ria" in self.url):
            for ref in raw_result:
                if all(elm in ref.get('href') for elm in ['html','http']):
                    refs.append(ref.get('href'))

        elif("tass" in self.url):
            for ref in raw_result:
                if re.search('[0-9]', ref.get('href')) and all(elm not in ref.get('href') for elm in ['http','press']):
                    refs.append(ref.get('href'))
            
        elif("interfax" in self.url):
            for ref in raw_result:
                if re.search('[0-9]', ref.get('href')) and  all(elm not in ref.get('href') for elm in ['http','photo','html','story','pressreleases']):
                 refs.append(ref.get('href'))

        else:
            pass

        return refs


    def get_parser_body(self,ref):
        """Returns 3 thousand characters of the text of the news in response
            to its address https://tass.ru/ref (example, '/politika/7999199')"""

        source = requests.get(f'{self.url}{ref}').text
        soup = Bs(source, 'lxml')
        raw_result = soup.find_all('div', class_='text-content')
        result = raw_result[0].text[:3000]

        return result







