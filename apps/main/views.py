from django.shortcuts import render
from django.http import HttpResponse
from apps.main.models import Anime
from .forms import AnimeNameForm
from django.db.models import Q


# Create your views here.
def index(request):
    if request.POST:
        form = AnimeNameForm(request.POST)

        print (form.data.get('anime_name'))

        if form.is_valid():
            anime = Anime.objects.filter(Q(title__icontains=form.data.get('anime_name')) |
                                         Q(title_eng__icontains=form.data.get('anime_name')))

            if anime:
                anime_data = anime[0].as_dict()
    else:
        form = AnimeNameForm()
        anime_data = Anime.objects.last().as_dict()

    data = {
        'form': form,
        'anime': anime_data
    }

    return render(request, 'index.html', data)
