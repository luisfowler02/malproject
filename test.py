import requests
from bs4 import BeautifulSoup
import time
from termcolor import colored
import random
from fake_useragent import UserAgent

url = "https://myanimelist.net/anime/33674/No_Game_No_Life__Zero"
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')
# ranked = soup.find('span', class_='numbers ranked')
# rank = ranked.find('strong').text
# rank = rank[1:]
ranked = soup.find('div', class_='spaceit_pad po-r js-statistics-info di-ib').text
rankest = float(ranked[8:13].strip())
rank = round(rankest, 2)
print(rank)

