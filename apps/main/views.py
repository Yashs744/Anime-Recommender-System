from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .handlers.recommend import get_similar
from .models import Anime, AnimeScore
from .forms import AnimeNameForm, AnimeScoreForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnimeScoreForm()

        if self.request.user.is_authenticated:
            username = self.request.user
            anime = self.get_object()

            user_score = AnimeScore.objects.filter(Q(username=username) & Q(anime=anime))
            if user_score:
                context['my_score'] = user_score.last().user_anime_score

        return context


class AnimeScoreView(LoginRequiredMixin, FormView):
    template_name = 'anime_detail.html'
    form_class = AnimeScoreForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()
        self.animeID = form.data.get('anime')

        if form.is_valid():
            self.form_valid(form)
        else:
            self.form_invalid(form)

        return self.get_success_url()

    def form_valid(self, form):
        form.instance.username = self.request.user
        form.save()

    def form_invalid(self, form):
        username = self.request.user
        anime = self.animeID

        obj = AnimeScore.objects.filter(Q(username=username) & Q(anime=anime))
        if obj:
            obj = obj.last()
            if obj.user_anime_score != form.data['user_anime_score']:
                obj.user_anime_score = form.data['user_anime_score']
                obj.save()

    def get_success_url(self):
        return HttpResponseRedirect(reverse('anime-detail', kwargs={'pk': self.animeID}))


class AnimeView(View):
    template_name = 'anime_detail.html'

    def get(self, request, *args, **kwargs):
        view = AnimeDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AnimeScoreView.as_view()
        return view(request, *args, **kwargs)


class RecommendView(TemplateView):

    template_name = 'recommend.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            anime = Anime.objects.get(anime_id=kwargs.get('pk'))

            anime_id = anime.anime_id
            anime_synopsis = anime.synopsis
        except Anime.DoesNotExist:
            raise Http404("Anime does not exist")

        similar_anime_ids = get_similar(anime_id=anime_id, anime_synopsis=anime_synopsis)
        similar_animes = Anime.objects.filter(anime_id__in=similar_anime_ids)

        context['animes'] = []
        for anime in similar_animes:
            context['animes'].append(anime.as_dict())

        return context