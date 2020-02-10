# Libraries
import traceback
from collections import OrderedDict
from recommender_system.recommendation import AnimeRecommendation
from recommender_system.helpers import df_to_html, read_data, update_data

# Path to the database
db_path = "/path/to/the/database.db"

# Variable to store SQL Queries
q = None

# Create a Connection to the Database
dataframe = read_data(database=db_path, query="SELECT * FROM Animes;")

# Initialize the Class
anime = AnimeRecommendation(dataframe)

# Get the Mappings
indices = anime.getMapping()

# Get Similarity Matrix
simMatrix = anime.getSimilartiyMatrix()


def homepage():
	"""
	Method to return top viewed animes for homepage.

	:return: ``JSON``, ``error``
	"""

	homepage_animes = OrderedDict([('animes', list())])

	try:
		q = "SELECT Anime_ID FROM Views ORDER BY vCount DESC LIMIT 10;"
		anime_ids = read_data(database=db_path, query=q)

		for idx in anime_ids['Anime_ID']:
			homepage_animes['animes'].append(anime.build_AnimeDict(idx))

		return homepage_animes, None

	except Exception as e:
		print(f"CODE 101:  {e}", flush = True)
		print(traceback.format_exc(), flush=True)
		print()

		return [], e


def available_animes():
	"""
	Method to convert pandas dataframe to html code.

	:return: ``HTML``, ``count``
		HTML CODE and Number of Animes in the database.
	"""

	count = dataframe.shape[0]
	df_html = df_to_html(dataframe[['Anime_ID', 'Title', 'Synopsis', 'Episodes', 'Premiered', 'Genre']])

	return df_html, count


def recommend_animes(anime_name):
	"""
	Method to recommend most similar animes based on the anime viewed.

	:param anime_name: ``string``
		Name of the viewed anime.

	:return: ``Ordered Dictionary``, ``error``
		Ordered Dictionary of recommended animes.
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

		return recommended_animes, None

	except Exception as e:
		print(f"CODE 102:  {e}", flush=True)
		print(traceback.format_exc(), flush=True)
		print()

		return [], e


def read_genre(genre):
	"""
	Method to read anime genre and return sample of animes that belong to the genre.

	:param genre: ``string``

	:return: ``Ordered Dictionary``, ``error``
		Ordered Dictionary of Animes.
	"""

	animes_by_genre = OrderedDict([('output', OrderedDict([('animes', list())]))])
	genre = genre.lower()

	try:
		anime_idxs = anime.getAnime_byGenre(genre)

		for idx in anime_idxs:
			animes_by_genre['output']['animes'].append(anime.build_AnimeDict(idx))

		return animes_by_genre, None

	except Exception as e:
		print(f"CODE 103:  {e}", flush=True)
		print(traceback.format_exc(), flush=True)
		print()

		return [], e


def add_count(anime_name):
	"""
	Create a View Count of the Anime Searched.

	:param anime_name: ``string``
		Name of the viewed anime.

	:return: ``HTTPS Status Code``, ``error``
		200 'Success'
	"""

	try:
		# Get the ID
		idx = anime.getID(anime_name.lower())[0]

		q = f"UPDATE Views SET vCount = vCount + 1 WHERE Anime_ID = {idx}"

		update_data(database=db_path, query=q)

		return 200

	except Exception as e:
		print(f"CODE 104:  {e}", flush=True)
		print(traceback.format_exc(), flush=True)
		print()

		return e


def autocomplete_title(term):
	"""

	:param term:
	:return:
	"""

	titles = dataframe[(dataframe.Title.str.contains(term, case=False))]['Title'].tolist()

	return titles
