from django.shortcuts import render
from django.views.generic import DetailView

from .models import Anime
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


class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'anime_detail.html'
    context_object_name = 'anime'
