from django import forms
from apps.main.models import AnimeScore


class AnimeNameForm(forms.Form):
    anime_name = forms.CharField(label="Anime Name", max_length=80)


class AnimeScoreForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnimeScoreForm, self).__init__(*args, **kwargs)

        self.fields['user_anime_score'].widget = forms.TextInput(attrs={
            'type': "number",
            'name': "user_anime_score",
            'id': "id_user_anime_score",
            'min': "1",
            'max': "10",
            'required': True,
        })

        self.fields['anime'].widget = forms.HiddenInput()

    class Meta:
        model = AnimeScore
        fields = ['anime', 'user_anime_score']
