'''
	Author: Yash Sharma
	Date: 22th May, 2018

	Third Party Tool Used: Jikan (https://github.com/jikan-me/jikan) as an API Endpoint of MAL.
'''

from fetch_anime import getTopAnimes, getSeasonalAnimes
import pandas as pd
import requests
import json
import time

def save_df(values, cols, filename):
	# Create a Pandas DataFrame & save it to the disk in CSV Format
	pd.DataFrame(values, columns = cols).to_csv(filename, index = False)

'''
# Top Animes

## Read the File that Contains Anime ID
df = getTopAnimes(start = 0, end = 1000, save_df = True)
id_list = list(df['IDx'])
title_list = list(df['Title'])

## Deleting df to save memory.
del df
'''

# Seasonal Animes

## Read the File that Contains Anime ID
df = pd.read_csv('AnimeList.csv')#getSeasonalAnimes()
id_list = list(df['IDx'])
title_list = list(df['Title'])
## Deleting df to save memory.
del df

# Base Url for fetching information.
BaseURL = "http://api.jikan.moe/anime/{}"

# ID, Title English, Synopsis, Episodes, Premiered, Genre, Rating, Score, Scored_By, Rank, Popularity, Members, Favorites, Image_URL
anime_content = list()

# failed anime IDs
anime_failed = list()

# for each anime ID in the list. do
for idx, title in zip(id_list, title_list):
	try:
		print (f"[-] Fetching Anime: ID {idx} - Title: {title}...")

		# Request for Anime Information with id = ID
		raw_content = requests.get(BaseURL.format(idx))

		# Checking whether response to the request is success or not
		if raw_content.status_code == 429:
			'''
				Reponse 429:
					Too Many Requests - You've either hit your daily limit or Jikan has hit the rate limit from MyAnimeList
			'''
			print ("[!] Too many Requests made...\n")
			print ("[!] Aborting....")

			# Abort the Process
			break

		# 200 - OK. Request was successful
		if raw_content.status_code == 200:

			print (f"[X] Data Fetched\n")
			print ("[-] Processing...")

			# pass the json response to JSON Object
			anime_json_data = json.loads(raw_content.content)

			# Checking whether reponse containts information or a error message
			if 'error' not in anime_json_data:

				# Get all the Genres related to the Anime
				genres = ", ".join([g['name'] for g in anime_json_data['genre']])

				# Tuple of Anime Information
				anime = (idx, anime_json_data['title'], str(anime_json_data['synopsis']),
					anime_json_data['episodes'], anime_json_data['premiered'], genres, anime_json_data['rating'],
					anime_json_data['score'], anime_json_data['scored_by'], anime_json_data['rank'],
					anime_json_data['popularity'], anime_json_data['members'], anime_json_data['favorites'],
					anime_json_data['image_url'])

				# Add the Tuple to the main list.
				anime_content.append(anime)

				# Anime Information Successfull ADDED.
				print ("[X] Success\n")

				# sleep for 1 sec
				time.sleep(0.5)

			else:
				# Display the Error Message
				print (f"[!] {anime_json_data['error']}")
				anime_failed.append((idx, title))
		else:
			print ("[!] Failed. Error Occured while Fetching Data\n")
			anime_failed.append((idx, title))

	except Exception as e:
		# Catch all the errors that can occur during the process
		# Display the Error and Continue the Process for next ID.
		print (f"[!] Processing Failed for ID: {idx}\n")
		print (f"[!!] ERROR: {e}\n\n")
		anime_failed.append((idx, title))
		continue

anime_cols = ["Anime_ID", "Title", "Synopsis", "Episodes", "Premiered", "Genre", "Rating", "Score", "Scored_By", "Rank", "Popularity", "Members", "Favorites", "Image_URL"]
failed_cols = ["IDx", "Title"]

save_df(values = anime_content, cols = anime_cols, filename = "anime.csv")
save_df(values = anime_failed, cols = failed_cols, filename = "failed_idx.csv")
