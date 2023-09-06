import requests
from bs4 import BeautifulSoup
import time
from termcolor import colored
import random
from fake_useragent import UserAgent
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['anime_db']
collection = db['animes']


class Anime:
    def __init__(self, rank, title, score, genres, image_link):
        self.rank = rank
        self.title = title
        self.score = score
        self.genres = genres
        self.image_link = image_link

    def display_details(self):
        print(f"Rank: {self.rank}")
        print(f"Title: {self.title}")
        print(f"Score: {self.score}")
        print(f"Genres: {','.join(self.genres)}")
        print(f"Image Link: {self.image_link}")

    @staticmethod
    # Scrapes all wanted data from each anime on a page and makes an object for each anime
    def scrape_from_myanimelist():
        score = 10
        base_url = "https://myanimelist.net/topanime.php"
        url_list = []
        anime_objects = []
        limit_num = 0
        num = 0

        user_agent = UserAgent()
        random_agent = user_agent.random
        headers = {'User-Agent': random_agent}

        while float(score) >= 8.00:
            # Takes all individual anime pages from each myanimelist top anime page
        
            url_list.append(base_url)
            html = requests.get(url_list[-1], headers=headers)
            soup = BeautifulSoup(html.content, "html.parser")
            animes_links = soup.find_all('h3', class_='fl-l fs14 fw-b anime_ranking_h3')
            href_list = []
            for link in animes_links:
                    link_tag = link.find('a')
                    if link_tag:
                            href = link_tag.get('href')
                            href_list.append(href)
            time.sleep(3)


            # Scrapes wanted data from each anime page
            for url in href_list:
                    html = requests.get(url)
                    soup = BeautifulSoup(html.content, 'html.parser')
                    score = soup.find(itemprop='ratingValue').text
                    if float(score) < 8.00:
                        break
                    title = soup.find('h1').text
                    ranked = soup.find('span', class_='numbers ranked')
                    rank = ranked.find('strong').text
                    rank = rank[1:]
                    genres = soup.find_all(itemprop='genre')
                    genre_list = []
                    for genre in genres:
                            genre_list.append(genre.text)
                    image_link = soup.find(itemprop='image')['data-src']
                    anime_obj = Anime(rank, title, score, genre_list, image_link)
                    anime_objects.append(anime_obj)
                    num = num + 1
                    print(rank)
                    print(title)
                    print(score)
                    print(genre_list)
                    print(image_link)
                    time.sleep(3)
            limit_num += 50
            base_url = 'https://myanimelist.net/topanime.php' + f'?limit={limit_num}'
            colored_text = colored(f'{num} objects have been created', 'red', attrs=['bold'])
            print(colored('-' * 40, 'white'))
            print(colored_text)
            print(colored('-' * 40, 'white'))


        return anime_objects