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

def getTopAnime(start = 0, end = 1000, save_df = True):
	"""[summary]

	Keyword Arguments:
		start {int} -- Fetch Anime from 'start'. (default: {0})
		end {int} -- Fetch Anime till 'end'. (default: {1000})
		save_df {bool} -- whether to save the dataframe to disk or not. (default: {True})

	returns:
		DataFrame of fetched Animes.
	"""
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
				id = ""

				try:
					all_a = top_animes[j].findAll('a')

					title = all_a[1].text
					link = all_a[1].get('href')
					id = re.search(r'/anime/([0-9]+)', link).group(1)

				except Exception as e:
					print (f"Error at {i+1}th Anime of {j}th List\n")

				anime_list.append((title, link, id))
		else:
			print(f"Couldnot load list {i}\n")

		time.sleep(1.5)

		df = pd.DataFrame(anime_list, columns = ['Titles', 'Links', 'IDs'])

	if save_df:
		df.to_csv('AnimeList.csv', sep=",", index = False, encoding = "utf8")

	return df

if __name__ == "__main__":
	getTopAnime()
