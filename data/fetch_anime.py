'''
	Author: Yash Sharma
	Date: 22th May, 2018

	Third Party Libraries Used:
		- requests to send request and get response
		- BeautifulSoup to parse the HTML Content.
		- pandas to create and manupilate dataframe.
'''

from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import time
import re

def save_toCSV(list_of_animes, cols = ['IDx', 'Title', 'Link'], to_disk = True):
	df = pd.DataFrame(list_of_animes, columns = cols)

	if to_disk:
		df.to_csv('AnimeList.csv', sep=",", index = False, encoding = "utf8")

	return df

def getTopAnimes(start = 0, end = 1000, save_df = True):
	anime_list = list()

	for i in range(start, end+1, 50):
		raw_content = requests.get(f"https://myanimelist.net/topanime.php?limit={i}")

		if (raw_content.status_code == 200):
			animes = BS(raw_content.text, 'lxml')

			animes = animes.find('div', {'class': 'pb12'})
			top_animes = animes.find('table', {'class': 'top-ranking-table'})
			top_animes = top_animes.findAll('tr', {'class': 'ranking-list'})

			for j in range(len(top_animes)):
				title = ""
				link = ""
				idx = ""

				try:
					all_a = top_animes[j].findAll('a')

					title = all_a[1].text
					link = all_a[1].get('href')
					idx = re.search(r'/anime/([0-9]+)', link).group(1)

				except Exception as e:
					print (f"Error at {i+1}th Anime of {j}th List\n")

				anime_list.append((id, title, link))
		else:
			print(f"Couldnot load list {i}\n")

		time.sleep(1.5)

	return save_toCSV(list_of_animes = anime_list, to_disk = save_df)

def getSeasonalAnimes(season = "winter", year = 2016, save_df = True):
	"""
		Hierarchy in the HTML Code:
			div.id = "content"
				- div.class: 'js-categories-seasonal'
					- div.class: js-seasonal-anime-list-key-1
					- div.class: js-seasonal-anime-list-key-2
					- div.class: js-seasonal-anime-list-key-3
					- div.class: js-seasonal-anime-list-key-4
					- div.class: js-seasonal-anime-list-key-5
					{
						6 div tags with keys 1, 2, 3, 4, 5
							key 1: TV
							key 2: OVA
							key 3: Movies
							key 4: Special
							key 5: ONA

						TV can have multiple div for diplaying continuing
					}
					Inside each key div
						- div.class: seasonal-anime (for each anime)
	"""

	# list of all the animes fetched from that season
	seasonal_anime_list = list()

	# Base URL for Seasonal Animes
	base_url = f"https://myanimelist.net/anime/season/{year}/{season}"

	# Send Requests using 'requests.get()' function
	r = requests.get(base_url)

	# if response is not OK abort the process.
	if r.status_code != 200:
		print (f"Status Code: {r.status_code}")
		abort(-1)

	# Parse the reponse using BS and htmlparser
	soup =  BS(r.text, 'html.parser')

	# Select all seasonal animes available in that season
	seasonal_animes = soup.find('div', id = "content").find('div', {'class': 'js-categories-seasonal'})

	# Selecting animes based on keys
	tv = seasonal_animes.find_all('div', {'class': 'js-seasonal-anime-list-key-1'})
	ova = seasonal_animes.find_all('div', {'class': 'js-seasonal-anime-list-key-2'})
	movies = seasonal_animes.find_all('div', {'class': 'js-seasonal-anime-list-key-3'})
	ona = seasonal_animes.find_all('div', {'class': 'js-seasonal-anime-list-key-5'})

	animes_byType = [tv, ova, movies, ona]
	for a_type in animes_byType:
		for i in range(len(a_type)):
			all_animes = a_type[i].find_all('div', {'class': 'seasonal-anime'})

			# for each anime
			anime_list = list()
			for i in range(len(all_animes)):
				# Select each anime one-by-one
				curr_anime = all_animes[i]

				link = title = curr_anime.find('p', {'class': 'title-text'}).a['href']
				idx = re.search(r'/anime/([0-9]+)', link).group(1)
				title = curr_anime.find('p', {'class': 'title-text'}).a.text

				anime = (idx, title, link)
				anime_list.append(anime)

			seasonal_anime_list.extend(anime_list)

	return save_toCSV(list_of_animes = seasonal_anime_list, to_disk = save_df)

if __name__ == "__main__":
	getTopAnimes()
