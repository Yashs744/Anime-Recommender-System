# Data Pipeline
import logging
import requests
from django.conf import settings
from apps.main.constants import ANIME_SEASONAL_YEAR, ANIME_SEASONAL_SEASONS
from apps.main.models import Anime, Genre

logger = logging.getLogger("data-handler")


def get_anime_info(anime):
    info = {
        'anime_id': anime['mal_id'],
        'title': anime['title'],
        'synopsis': anime['synopsis'],
        'episodes': anime['episodes'],
        'score': anime['score'],
        'members': anime['members'],
        'source': anime['source'],
        'image': anime['image_url'],
    }

    return info


def seasonal_anime_search(year, season):
    """
    :param year:
    :param season:
    :return:
    """

    assert year in ANIME_SEASONAL_YEAR and season in ANIME_SEASONAL_SEASONS, f"{year} - {season} not available"

    url = settings.ANIME_SEASON_URL + f"{year}/{season}/"
    resp = requests.get(url)

    if resp.status_code == requests.codes.ok:
        resp = resp.json()['anime']

        for anime in resp:
            try:
                info = get_anime_info(anime)

                anime_obj = Anime.objects.create(**info)
                genre_objs = (Genre(anime=anime_obj, name=genre['name']) for genre in anime['genres'])
                anime_obj.genre.bulk_create(genre_objs)
            except Exception as e:
                logger.error(e)
    else:
        logger.info(f"{resp.status_code}")


def search_anime(name: str):
    """
    :param name:
    :return:
    """
    data = {
        'anime_id': None,
        'title': None,
        'synopsis': None,
        'score': None,
        'episodes': None,
        'image': None,
    }

    search_url = settings.ANIME_SEARCH_URL + name
    resp = requests.get(search_url)

    if resp.status_code == requests.codes.ok:
        resp = resp.json()['results']

        for i in range(len(resp)):
            anime = resp[i]

            data['anime_id'] = anime['mal_id']
            data['title'] = anime['title']
            data['synopsis'] = anime['synopsis']
            data['score'] = anime['score']
            data['image'] = anime['image_url']
            data['episodes'] = anime['episodes']

            try:
                Anime.objects.create(**data)
            except Exception as e:
                print(e)
    else:
        logger.info(f"{resp.status_code}")

    return data

