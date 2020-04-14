# Data Pipeline
import logging
import requests
import time
from django.conf import settings
from apps.main.constants import ANIME_SEASONAL_YEAR, ANIME_SEASONAL_SEASONS
from apps.main.models import Anime, Genre
from django.db.models import Q

logger = logging.getLogger("data-handler")


def retrieve_anime_info(anime: dict):
    """
    :param anime:
    :return:
    """

    info = {
        'anime_id': anime['mal_id'],
        'title': anime['title'],
        'title_eng': anime['title_english'] if anime.get('title_english', None) else '',
        'synopsis': anime['synopsis'],
        'episodes': anime['episodes'] if anime.get('episodes', None) else None,
        'rating': anime['rating'] if anime.get('rating', None) else '',
        'score': anime['score'],
        'scored_by': anime['scored_by'] if anime.get('scored_by', None) else None,
        'rank': anime['rank'] if anime.get('rank', None) else None,
        'popularity': anime['popularity'] if anime.get('popularity', None) else None,
        'members': anime['members'] if anime.get('members', None) else None,
        'source': anime['source'] if anime.get('source', None) else '',
        'image': anime['image_url'],
        'genres': [genre['name'] for genre in anime['genres']] if anime.get('genres', None) else [],
    }

    return info


def get_anime(anime_id: int, ignore_check: bool = False):
    """
    :param anime_id:
    :param ignore_check:
    :return:
    """

    anime_info = None
    search_url = f'{settings.JIKAN_BASE_URL}/anime/{anime_id}'

    anime_exist = Anime.objects.filter(anime_id=anime_id)

    if ignore_check or (anime_exist and not anime_exist.last().genre.all()):
        resp = requests.get(search_url)

        if resp.status_code == requests.codes.ok:
            resp = resp.json()

            anime_data = retrieve_anime_info(anime=resp)
            data = anime_data.copy()
            data.pop('genres')

            Anime.objects.update_or_create(anime_id=anime_id, defaults=data)
            obj = Anime.objects.get(anime_id=anime_id)
            if anime_data['genres']:
                genre_objs = (Genre(anime=obj, name=genre) for genre in anime_data['genres'])
                obj.genre.bulk_create(genre_objs)

            anime_info = obj.as_dict()
            time.sleep(4)
        else:
            logger.info(resp.status_code)

    return anime_info


def fetch_animes(name: str):
    """
    Method to fetch anime which doesn't exist in the database currently.

    :param name:
    :return:
    """

    anime_list = list()

    search_url = settings.ANIME_SEARCH_URL + name
    resp = requests.get(search_url)

    if resp.status_code == requests.codes.ok:
        resp = resp.json()['results']

        for anime in resp[:10]:
            try:
                data = get_anime(anime_id=anime['mal_id'], ignore_check=True)
                if data:
                    anime_list.append(data)
            except Exception as e:
                logger.debug(e)
    else:
        logger.info(resp.status_code)

    return anime_list


def search_anime(anime_name: str):
    """
    Method to search the anime or list of animes from the database.

    :param anime_name:
    :return:
    """

    anime_list = list()

    animes = Anime.objects.filter(Q(title__icontains=anime_name) |
                                  Q(title_eng__icontains=anime_name))

    if animes.exists():
        for anime in animes:
            new_info = get_anime(anime_id=anime.anime_id)

            data = new_info if new_info else anime.as_dict()
            anime_list.append(data)
    else:
        anime_list = fetch_animes(name=anime_name)

    if len(anime_list) == 0:
        anime_list = [anime.as_dict() for anime in Anime.objects.order_by('-score')[:10]]

    return anime_list


