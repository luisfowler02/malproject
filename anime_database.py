import pymongo
from anime import Anime
from termcolor import colored

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['anime_db']
collection = db['animes']

def insert_anime_objects(anime_objects):
	inserted_check = 0
	for anime_obj in anime_objects:
		doc = {

		'rank': anime_obj.rank,
		'title': anime_obj.title,
		'score': anime_obj.score,
		'genres': anime_obj.genres

		}

		verify = collection.find_one({'title': anime_obj.title})

		if verify is None:
			collection.insert_one(doc)
			inserted_check += 1

	colored_text = colored(f'{inserted_check} have been inputted', 'red', attrs=['bold'])
	print(colored_text)
	print(colored('-' * 40, 'white'))


if __name__ == '__main__':
	anime_list = Anime.scrape_from_myanimelist()
	insert_anime_objects(anime_list)
	color_text = colored('Database Insertion Complete', 'red', 'on_green')
	print(color_text)

