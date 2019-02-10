from flask import render_template
from app import application
from app.helper import render_homepage, render_available_anime, \
    get_anime_and_return_recommended, get_genre_and_return_response, get_term_and_autocomplete


@application.route('/')
def home():
    """
    Method to render home.html

    :return: ``HTML Page``
    """

    return render_template('home.html')


@application.route('/homepage', methods=['GET'])
def homepage():
    """
    :return: ``JSON``
    """

    return render_homepage()


@application.route('/recommend/<string:anime_name>', methods=['GET'])
def recommend(anime_name):
    """
    :param anime_name: ``string``
        Name of the Anime.

    :return: ``JSON``
    """

    anime_name = anime_name.strip()
    return get_anime_and_return_recommended(anime_name)


@application.route('/available_animes', methods=['GET'])
def available_animes():
    """
    :return: ``HTML``
    """

    return render_available_anime()


@application.route('/genres/<string:genre>', methods=['GET'])
def genres(genre):
    """
    :param genre: ``string``

    :return: ``string``
    """

    genre = genre.strip()
    return get_genre_and_return_response(genre)


@application.route('/autocomplete/<string:term>', methods=['GET'])
def autocomplete(term):
    """

    :param term:
    :return:
    """

    return get_term_and_autocomplete(term)


@application.route('/404')
def not_found():
    """
    :return: ``HTML Page``
    """

    return render_template('404.html')
