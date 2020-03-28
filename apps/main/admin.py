from django.contrib import admin
from apps.main.models import Genre, Anime


# Register your models here.
class GenreInline(admin.StackedInline):
    model = Genre


class AnimeAdmin(admin.ModelAdmin):
    inlines = [
        GenreInline
    ]


admin.site.register(Anime, AnimeAdmin)