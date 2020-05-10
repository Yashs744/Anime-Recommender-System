from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserAuthenticationForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
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
    return render(request, 'profile.html')
