'''
	Author: Yash Sharma
	Date: 22th May, 2018

	Third Party Tool Used: Jikan (https://github.com/jikan-me/jikan) as an API Endpoint of MAL.
'''

import pandas as pd
import requests
import json
import time

from fetch_anime import getTopAnimes, getSeasonalAnimes
from preprocess import cleanSynopsis, cleanTitle, processSynopsis, processRatings
import sqlite3 as sql

# Top Anime / Seasonal Animes

## Read the dataframe that contains Anime ID
df = getSeasonalAnimes(season = "fall", year = 2017)
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

				# sleep for 1/2 sec
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

anime_df = pd.DataFrame(anime_content, columns = anime_cols)
failed_df = pd.DataFrame(anime_failed, columns = failed_cols)

# Apply Cleaning Steps
anime_df['Title'] = anime_df.Title.apply(cleanTitle)
anime_df['Synopsis'] = anime_df.Synopsis.apply(cleanSynopsis)

# New Columns 'c' stands for cleaned & preprocessed
anime_df['cSynopsis'] = anime_df.Synopsis.apply(processSynopsis)
anime_df['cGenre'] = anime_df.Genre.str.lower()
anime_df['cRating'] = anime_df.Rating.apply(processRatings)

#Create an in-memory SQLlite Database
conn = sql.connect('dataset.db')

# save to the database
try:
	anime_df.to_sql(name = 'Animes', con = conn, index = False, if_exists = 'append')
except:
	existing = pd.read_sql_query('SELECT Anime_ID FROM Animes', con = conn)
	mask = ~anime_df.Anime_ID.isin(existing.Anime_ID)

	try:
		anime_df.loc[mask].to_sql(name = 'Animes', con = conn, index = False, if_exists = 'append')
	except Exception as e:
		print (f"[!] {e}")

conn.close()