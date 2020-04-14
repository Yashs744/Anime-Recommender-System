from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserAuthenticationForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.changed_data[0]
            messages.success(request, f'Account Registered for {username}!')
            return redirect('login')
    else:
        form = UserAuthenticationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')
