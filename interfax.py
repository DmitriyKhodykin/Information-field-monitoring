# Модуль для разбора новостной ленты "Интерфакс"
# pip install lxml

# Импорты
import requests
from bs4 import BeautifulSoup
import pandas as pd


def interfax():
    """Возвращает заголовки новостей с главной страницы Интерфакс"""
    source = requests.get('https://www.interfax.ru/russia/').text
    soup = BeautifulSoup(source, 'lxml')

    news_list = []
    
    # Блок главный новостей
    for main_line in soup.find_all('div', class_='newsmain'):
        news_main = main_line.h3.text.split('/')
        for item in news_main:
            news_list.append(item)
    
    # Блок новостной ленты
    for time_line in soup.find_all('div', class_='timeline__group'):
        news_line = time_line.h3.text.split('/')
        for item in news_line:
            news_list.append(item)

    # Блок главных новостей под фото
    for photo_line in soup.find_all('div', class_='timeline__photo'):
        photo_news = photo_line.h3.text.split('/')
        for item in photo_news:
            news_list.append(item)

    # Еще один блок ленты новостей
    for text_line in soup.find_all('div', class_='timeline__text'):
        text_news = text_line.h3.text.split('/')
        for item in text_news:
            news_list.append(item)

    df_interfax = pd.DataFrame(news_list)
    return df_interfax
