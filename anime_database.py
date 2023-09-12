import pymongo
from anime import Anime
from termcolor import colored
from random import choice
import os

mongo_uri = os.environ.get('MONGO_URI')
mongo_username = os.environ.get('MONGO_USERNAME')
mongo_password = os.environ.get('MONGO_PASSWORD')

client = pymongo.MongoClient(mongo_uri, username=mongo_username, password=mongo_password)
db = client['Cluster0']
collection = db['animes']

def insert_anime_objects(anime_objects):
	inserted_check = 0
	for anime_obj in anime_objects:
		doc = {

		'rank': anime_obj.rank,
		'title': anime_obj.title,
		'score': anime_obj.score,
		'genres': anime_obj.genres,
		'image link' : anime_obj.image_link

		}

		verify = collection.find_one({'title': anime_obj.title})

		if verify is None:
			collection.insert_one(doc)
			inserted_check += 1

	colored_text = colored(f'{inserted_check} have been inputted', 'red', attrs=['bold'])
	print(colored_text)
	print(colored('-' * 40, 'white'))

def get_anime_by_genre(genre):
	query = {'genres': genre}
	animes = list(collection.find(query))
	random_anime = choice(animes)
	return random_anime

def update_database():
	anime_list = Anime.scrape_from_myanimelist()
	insert_anime_objects(anime_list)
	color_text = colored('Database Insertion Complete', 'red', 'on_green')
	print(color_text)