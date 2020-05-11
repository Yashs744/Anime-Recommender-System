from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserAuthenticationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input100'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']
