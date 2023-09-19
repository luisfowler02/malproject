import requests
from bs4 import BeautifulSoup
import time
from termcolor import colored
import random
from fake_useragent import UserAgent
from jikanpy import Jikan
import json

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

        while float(score) >= 7.00:
            # Takes all individual anime pages from each myanimelist top anime page
            try:
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
            except:
                print('HTML structure likely changed on top anime page')
                
            time.sleep(3)


            # Scrapes wanted data from each anime page
            for url in href_list:
                    html = requests.get(url)
                    soup = BeautifulSoup(html.content, 'html.parser')
                    score = soup.find(itemprop='ratingValue').text
                    if float(score) < 7.00:
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

    def get_seasonal_anime():
        anime_objects = []
        url = 'https://api.jikan.moe/v4/seasons/now'
        html = requests.get(url)
        json_data = BeautifulSoup(html.content,'html.parser')
        json_data = f'{json_data}'
        data = json.loads(json_data)
        # formatted_json = json.dumps(data,indent=4)
        # print(formatted_json)
        anime_list = data['data']
        for anime_data in anime_list:
            title = anime_data['title']
            rank = anime_data['rank']
            score = anime_data['score']
            image_dict = anime_data['images']
            jpg_dict = image_dict['jpg']
            image_link = jpg_dict['image_url']
            if score == None:
                score = 'N/A'
            print(f'Title: {title}')
            print(f'Rank: {rank}')
            genre_list = []
            for genre in anime_data['genres']:
                name = genre['name']
                genre_list.append(name)
            for theme in anime_data['themes']:
                name_2 = theme['name']
                genre_list.append(name_2)
            print(f'Genres: {genre_list}')
            print(f'Score: {score}')
            print(f'Image Link: {image_link}')
            print('-' * 40)
            anime_obj = Anime(rank, title, score, genre_list, image_link)
            anime_objects.append(anime_obj)

        return anime_objects