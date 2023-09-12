# import requests
# from bs4 import BeautifulSoup
# import time
# from termcolor import colored
# import random
# from fake_useragent import UserAgent

# url = "https://myanimelist.net/topanime.php"
# html = requests.get(url)
# soup = BeautifulSoup(html.content, 'html.parser')
# animes_links = soup.find_all('h3', class_='fl-l fs14 fw-b anime_ranking_h3')
# href_list = []
# for link in animes_links:
#         link_tag = link.find('a')
#         if link_tag:
#                 href = link_tag.get('href')
#                 href_list.append(href)
# print(f'Anime Links: {href_list}')

import pymongo
from anime import Anime
from termcolor import colored
from random import choice

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['anime_db']
collection = db['animes']

query = {"genres": {"$in": ["Ecchi"]}}

count = collection.count_documents(query)

print(f'Number of documents with ecchi as a genre: {count}')


