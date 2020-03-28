from django.core.validators import MinLengthValidator
from django.db import models


class Anime(models.Model):
    class Meta:
        verbose_name = "anime info"

    anime_id = models.IntegerField(verbose_name='ID of Anime', primary_key=True, db_index=True)

    title = models.CharField(verbose_name="Title in Japanese", max_length=100)
    title_eng = models.CharField(verbose_name="Title in English", max_length=100, blank=True, null=True)

    synopsis = models.TextField(verbose_name="Summary (Synopsis)", validators=[MinLengthValidator(limit_value=100)])

    episodes = models.IntegerField(verbose_name="Number of Episodes")

    premiered = models.TextField(verbose_name="Premiered", blank=True)

    rating = models.TextField(verbose_name="Ratings", blank=True)

    score = models.FloatField(verbose_name="Weighted Score", null=True)
    scored_by = models.IntegerField(verbose_name="Scored By", null=True)

    rank = models.IntegerField(verbose_name="Overall Rank")
    popularity = models.IntegerField(verbose_name="Overall Popularity")

    image = models.URLField(verbose_name="Image URL")

    def as_dict(self):
        data = {
            'id': self.anime_id,
            'name': self.title,
            'name_english': self.title_eng,
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