from django.urls import path
from apps.main import views
from apps.main.views import AnimeView, RecommendView

urlpatterns = [
    path('', views.index, name='index'),
    path('anime/<int:pk>', AnimeView.as_view(), name='anime-detail'),
    path('recommend/<int:pk>', RecommendView.as_view(), name='recommend-anime'),
]
