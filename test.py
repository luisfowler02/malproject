import pymongo
from anime import Anime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['anime_db']
collection = db['animes']

def insert_anime_objects(anime_objects):
	for anime_obj in anime_objects:
		doc = {

		'rank': anime_obj.rank,
		'title': anime_obj.title,
		'score': anime_obj.score,
		'genres': anime_obj.genres

		}

result = collection.find({'title': 'Fruits Basket: The Final'})


