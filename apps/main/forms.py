from django import forms


class AnimeNameForm(forms.Form):
    anime_name = forms.CharField(label="Anime Name", max_length=80)
