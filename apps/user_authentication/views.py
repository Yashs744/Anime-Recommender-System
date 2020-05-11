from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserAuthenticationForm, UserProfileUpdateForm, UserUpdateForm
from ..main.models import AnimeScore


def register(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            form.instance.slug = form.cleaned_data['username']
            form.save()

            username = form.changed_data[0]
            messages.success(request, f'Account Registered for {username}! You are now logged in!')

            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('index')
    else:
        form = UserAuthenticationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    username = request.user
    objects = AnimeScore.objects.filter(username=username)

    if objects:
        context['animes'] = []
        objects = objects.order_by('-user_anime_score')
        for i, obj in enumerate(objects):
            anime = obj.as_dict()
            anime['num'] = i+1
            context['animes'].append(anime)

    return render(request, 'profile.html', context)
