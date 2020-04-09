from django.shortcuts import render
from django.http import HttpResponse
from apps.main.models import Anime
from .forms import AnimeNameForm
from django.db.models import Q
from .handlers.base import search_anime


# Create your views here.
def index(request):
    anime_data = ''

    if request.POST:
        form = AnimeNameForm(request.POST)

        if form.is_valid():
            anime_name = form.data.get('anime_name')

            anime = Anime.objects.filter(Q(title__icontains=anime_name) | Q(title_eng__icontains=anime_name))
            if anime:
                anime_data = anime[0].as_dict()
            else:
                anime_data = search_anime(name=anime_name)

    else:
        form = AnimeNameForm()

    data = {
        'form': form,
        'anime': anime_data
    }

    return render(request, 'index.html', data)
