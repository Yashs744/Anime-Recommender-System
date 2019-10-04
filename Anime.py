# Libraries
import pandas as pd
from collections import OrderedDict
from Recommendation import AnimeRecommendation
from flask import make_response, jsonify
import sqlite3 as sql

# Create a Connection to the Database
conn = sql.connect("data/dataset.db")
# Load the Dataset
dataframe = pd.read_sql_query("SELECT * FROM Animes;", con=conn)
dataframe = dataframe.reset_index()
dataframe = dataframe.drop('index', axis=1)

# Initialize the Class
anime = AnimeRecommendation(dataframe)

# Get the Mappings
indices = anime.getMapping()

# Get Similarity Matrix
simMatrix = anime.getSimilartiyMatrix()


def homePage():
	"""
		:return:
			JSON Formatted response of anime or 404 Error.

	"""

	homepage_animes = OrderedDict([('animes', list())])

	try:
		conn = sql.connect("data/dataset.db")
		anime_idxs = pd.read_sql_query("SELECT Anime_ID FROM Views ORDER BY vCount DESC LIMIT 10;", con=conn)

		for idx in anime_idxs['Anime_ID']:
			homepage_animes['animes'].append(anime.build_AnimeDict(idx))

		return homepage_animes
	except Exception as e:
		return make_response(jsonify({'Success': False}), 404)


def returnRecommended(anime_name):
	"""
		Parameters:
			anime_name: Name of the Anime to get Recommendation.

		:return:
			JSON Formatted response of recommended anime.
	"""

	recommended_animes = OrderedDict()

	recommended_animes['input'] = list()
	recommended_animes['output'] = OrderedDict()
	recommended_animes['output']['animes'] = list()

	anime_name = anime_name.lower()

	anime_Idx = anime.getID(anime_name)

	try:
		if len(anime_Idx) > 1:
			for idx in anime_Idx:
				recommended_animes['output']['animes'].append(anime.build_AnimeDict(idx))

		else:
			# Get Anime ID
			anime_id = anime.getID(anime_name)[0]
			recommended_animes['input'].append(anime.build_AnimeDict(anime_id))

			g = anime.getRecommendation(anime_id, simMatrix, indices)

			for idx in g:
				recommended_animes['output']['animes'].append(anime.build_AnimeDict(idx))

		return recommended_animes
	except Exception as e:
		return make_response(jsonify({'Success': False}), 404)


def readGenre(genre):
	"""
		Parameters:
			genre: One of the Genres.

		:return:
			JSON Formatted reponse with animes.
	"""
	animes_by_genre = OrderedDict([
		('output', OrderedDict([
			('animes', list())
		]))
	])
	genre = genre.lower()

	try:
		anime_idxs = anime.getAnime_byGenre(genre)

		for idx in anime_idxs:
			animes_by_genre['output']['animes'].append(anime.build_AnimeDict(idx))

		return animes_by_genre
	except Exception as e:
		return make_response(jsonify({'Success': False}), 404)


def addCount(anime_name):
	"""
		Create a View Count of the Anime Searched.

		Parameters:
			anime_name: JSON Formatted Data with Name of the searched Anime.

		:return:
			201 Succes
	"""
	try:
		# Get the ID
		idx = anime.getID(anime_name.get("anime_name", None).lower())[0]

		conn = sql.connect("data/dataset.db")

		cur = conn.cursor()
		cur.execute(f"UPDATE Views SET vCount = vCount + 1 WHERE Anime_ID = {idx}")

		conn.commit()

		return 201
	except Exception as e:
		with open("log.txt", "a") as log:
			log.write(str(e))
