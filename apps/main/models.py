from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Anime(models.Model):
    class Meta:
        verbose_name = "anime info"

    anime_id = models.IntegerField(verbose_name='ID of Anime', primary_key=True, db_index=True)

    title = models.CharField(verbose_name="Title in Japanese", max_length=100)
    title_eng = models.CharField(verbose_name="Title in English", max_length=100, blank=True, null=True)

    synopsis = models.TextField(verbose_name="Summary (Synopsis)", validators=[MinLengthValidator(limit_value=100)])

    episodes = models.IntegerField(verbose_name="Number of Episodes", blank=True, null=True)

    premiered = models.TextField(verbose_name="Premiered", blank=True)

    rating = models.TextField(verbose_name="Ratings", blank=True)

    score = models.FloatField(verbose_name="Weighted Score", null=True, blank=True)
    scored_by = models.IntegerField(verbose_name="Scored By", null=True, blank=True)

    rank = models.IntegerField(verbose_name="Overall Rank", null=True)
    popularity = models.IntegerField(verbose_name="Overall Popularity", null=True, blank=True)
    members = models.IntegerField(verbose_name="Members", null=True)

    source = models.CharField(verbose_name="Source of Anime", max_length=25, null=True)

    image = models.URLField(verbose_name="Image URL")

    def as_dict(self):
        data = {
            'id': self.anime_id,
            'title': self.title,
            'title_english': self.title_eng,
            'synopsis': self.synopsis,
            'episodes': self.episodes,
            'score': self.score,
            'scored_by': self.scored_by,
            'image': self.image,
            'genres': []
        }

        genres = self.genre.all()
        for genre in genres:
            data['genres'].append(genre.name)

        return data

    def __str__(self):
        return f"{self.anime_id} {self.title}"


class Genre(models.Model):
    class Meta:
        verbose_name = "anime genre"

    anime = models.ForeignKey(Anime, verbose_name="anime info", related_name="genre", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name of Genre", max_length=20)

    def __str__(self):
        return f"{self.name}"


class AnimeScore(models.Model):
    class Meta:
        verbose_name = "anime score"

    anime = models.OneToOneField(Anime, verbose_name="Anime", related_name="anime_score", on_delete=models.CASCADE,
                                 primary_key=True)
    username = models.ForeignKey(User, verbose_name="User", related_name="user_score", on_delete=models.CASCADE)
    user_anime_score = models.IntegerField(verbose_name="My Score")

    def __str__(self):
        return f"{self.username.username} - {self.anime.title}:{self.user_anime_score}"
