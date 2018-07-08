'''
	Author: Yash Sharma
	Date: 22th May, 2018

	Third Party Tool Used: Jikan (https://github.com/jikan-me/jikan) as an API Endpoint of MAL.
'''

from fetch_anime import *
import json

# Base Url for fetching information.
BaseURL = "http://api.jikan.moe/anime/{}"

# ID, Title English, Syponsis, Episodes, Premiered, Genre, Rating, Score, Scored_By, Rank, Popularity, Members, Favorites
anime_content = list()

# Read the File that Contains Anime ID
df = pd.read_csv('AnimeList.csv')
id_list = list(df['IDs'])
# Deleting df to save memory.
del df

# for each anime ID in the list. do
for ID in id_list:
	try:
		print (f"[-] Fetching Anime with ID {ID}...")

		# Request for Anime Information with id = ID
		raw_content = requests.get(BaseURL.format(ID))

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
				anime = (ID, anime_json_data['title'], str(anime_json_data['synopsis']),
					anime_json_data['episodes'], anime_json_data['premiered'], genres, anime_json_data['rating'],
					anime_json_data['score'], anime_json_data['scored_by'], anime_json_data['rank'],
					anime_json_data['popularity'], anime_json_data['members'], anime_json_data['favorites'])

				# Add the Tuple to the main list.
				anime_content.append(anime)

				# Anime Information Successfull ADDED.
				print ("[X] Success\n")

			else:
				# Display the Error Message
				print (f"[!] {anime_json_data['error']}")
		else:
			print ("[!] Failed. Error Occured while Fetching Data\n")

	except Exception as e:
		# Catch all the errors that can occur during the process
		# Display the Error and Continue the Process for next ID.
		print (f"[!] Processing Failed for ID: {ID}\n")
		print (f"[!!] ERROR: {e}\n\n")
		continue


# Create a Pandas DataFrame for the anime information collected
df = pd.DataFrame(anime_content,
	columns = ["ID", "Title", "Syponsis", "Episodes", "Premiered", "Genre", "Rating", "Score", "Scored_By", "Rank", "Popularity", "Members", "Favorites"])

# Save the DataFrame as an CSV File.
df.to_csv('Anime.csv', index = False)
