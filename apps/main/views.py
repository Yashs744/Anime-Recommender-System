from django.shortcuts import render
from .forms import AnimeNameForm
from .handlers import search_anime


# Create your views here.
def index(request):
    """
    :param request:
    :return:
    """

    data = dict()

    if request.POST:
        form = AnimeNameForm(request.POST)
        if form.is_valid():
            if 'search' in form.data:
                animes: list = search_anime(anime_name=form.data.get('anime_name'))
                data['animes'] = animes
    else:
        form = AnimeNameForm()

    data['form'] = form
    return render(request, 'index.html', data)
