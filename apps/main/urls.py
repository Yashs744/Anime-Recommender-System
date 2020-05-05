from django.urls import path
from apps.main import views
from apps.main.views import AnimeDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('anime/<int:pk>', AnimeDetailView.as_view(), name='anime-detail'),
]
