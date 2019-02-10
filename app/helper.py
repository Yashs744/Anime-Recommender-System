from app.constants import ErrorCodes
from app.errors import error_response
from flask import render_template, jsonify
from http import HTTPStatus
from recommender_system.anime import add_count, autocomplete_title, available_animes, \
    homepage, read_genre, recommend_animes


def render_homepage():
    """
    Method to render animes for homepage.

    :return: ``JSON``
    """

    homepage_animes, err = homepage()

    return return_response(response_data=homepage_animes, response_error=err)


def render_available_anime():
    """
    Method to render the available anime page.

    :return:
    """

    output_html, count = available_animes()

    return render_template('animes.html',
                           tables=[output_html],
                           a_count=count)


def get_anime_and_return_recommended(anime_name):
    """
    Method to read the name of searched anime and return animes which are most similar to it.

    :param anime_name:
        Name of the searched anime.

    :return: ``JSON``
    """

    animes, err = recommend_animes(anime_name)
    resp = add_count(anime_name)

    return return_response(response_data=animes, response_error=err)


def get_genre_and_return_response(genre):
    """
    Method to read genre and return sample of animes in that genre.

    :param genre: ``string``

    :return: ``JSON``
    """

    animes, err = read_genre(genre=genre)

    return return_response(response_data=animes, response_error=err)


def get_term_and_autocomplete(term):
    """

    :param term:
    :return:
    """

    return jsonify(title_list=autocomplete_title(term)), 200


def return_response(response_data, response_error):
    """
    Method to return json formatted response or error response.

    :param response_data: ``Ordered Dictonary or List of Animes``
    :param response_error: ``string``
        None or error message.

    :return: ``JSON``
    """
    # failed reading transactions
    if response_error or len(response_data) == 0:
        return error_response(error_code=ErrorCodes.METHOD_NOT_ALLOWED,
                              status_code=HTTPStatus.BAD_REQUEST.value)

    return jsonify(
        status='success',
        data=response_data), 200
