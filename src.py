import collections
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import random

def scrap_data():
  url = 'https://www.scientificamerican.com/the-sciences/'
  response = requests.get(url)
  response.encoding = 'utf-8'
  value = response.text
  soup = BeautifulSoup(value,'lxml')
  state = soup.find('ul',class_ = 'header-topic-list landing-header__nav__list')
  topics = state.find_all('li',class_ = 'landing-header__nav__list__item')
  limit = 100
  print(len(topics))
  for topic in topics:
    arr = []
    current_topic_href= topic.a['href']
    current_topic_text = topic.a.text
    print(current_topic_text)
    response = requests.get(current_topic_href)
    response.encoding = 'utf-8'
    value = response.text
    soup = BeautifulSoup(value,'lxml')
    state = soup.find('ol',class_ = 'pagination__nums')
    pages = state.find_all('li')
    number_of_pages = int(pages[-1].text)
    for k in range(number_of_pages):
      current_page_link = current_topic_href + '?page=' + str(k + 1)
      response = requests.get(current_page_link)
      response.encoding = 'utf-8'
      value = response.text
      soup = BeautifulSoup(value,'lxml')
      all_article_pages = soup.find_all('div',class_='listing-wide__inner')
      for article_page in all_article_pages:
        article_link = article_page.a['href']
        title = article_page.a.text 
        response = requests.get(article_link)
        response.encoding = 'utf-8'
        value = response.text
        soup = BeautifulSoup(value,'lxml')
        divParagraph = soup.find_all('div',class_='mura-region-local')
        video_state = soup.find('div',class_='podcasts-media podcasts-media--feature podcasts__media')
        if video_state is not None:
          continue
        article_text = ''
        for div in divParagraph:
          paragraph = div.find_all('p')
          for p in paragraph:
            article_text+=p.text
        arr.append([article_text,title])
        print(len(arr))
        if len(arr) == limit:
          df = pd.DataFrame(arr,columns = ['articleText','title'])
          file_idx = random.randint(1,10000)
          folder_name = '/content/drive/MyDrive/dataset/science dataset/{}'.format(current_topic_text)
          if os.path.exists(folder_name) == False:
            os.mkdir(folder_name)
          path = folder_name + '/{}.csv'.format(str(file_idx))
          df.to_csv(path)
          arr = []
