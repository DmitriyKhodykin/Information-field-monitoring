# Модуль для разбора новостной ленты "Риа"
# pip install lxml

# Импорты
import requests
from bs4 import BeautifulSoup
import pandas as pd


def ria():
    """Возвращает заголовки новостей с главной Риа.ру"""
    source = requests.get('https://www.ria.ru').text
    soup = BeautifulSoup(source, 'lxml')

    news_list = []
    for main_line in soup.find_all('span', class_='cell-list__item-desc'):
        news_main = main_line.span.text.split('/')
        for item in news_main:
            news_list.append(item)

    df_ria = pd.DataFrame(news_list)
    return df_ria
