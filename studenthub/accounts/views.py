import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from .forms import SignUpForm
from .models import Profile


def home_view(request):
    return render(request, 'home.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after signup
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome to StudentHub, {username}! Your account has been created successfully.')
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    # Apply Bootstrap classes to form fields
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def choose_avatar(request):
    if request.method == 'POST':
        selected_avatar = request.POST.get('avatar')
        if selected_avatar:
            # Get or create profile for the user
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            # Update avatar
            profile.avatar = selected_avatar
            profile.save()
            
            messages.success(request, 'Avatar updated successfully!')
            return redirect('home')
    
    # Get available avatars from media/avatars directory
    avatars_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    available_avatars = []
    
    if os.path.exists(avatars_dir):
        for filename in os.listdir(avatars_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                available_avatars.append(f'avatars/{filename}')
    
    # Ensure default avatar is always available
    if 'avatars/default.png' not in available_avatars:
        available_avatars.append('avatars/default.png')
    
    return render(request, 'choose_avatar.html', {'avatars': available_avatars})
