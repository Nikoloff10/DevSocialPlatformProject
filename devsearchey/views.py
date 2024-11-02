from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from devsearchey.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')






def profile_view(request):
    if request.method == 'POST':
        if 'delete_profile' in request.POST:
            request.user.profile.delete()
            request.user.delete()
            return redirect('home')
        else:
            form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)

    avatar_url = form.instance.avatar.url if form.instance.avatar else '/media/avatars/default.jpg'
    return render(request, 'profile.html', {'form': form, 'avatar_url': avatar_url})