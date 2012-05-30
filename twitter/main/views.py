# -.- coding:utf8 -.-
from main.models import Profile
from django.contrib.auth.models import User
from main.forms import UserCreateForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def index(request):
    return render_to_response('index.html')


def sign_up(request):
    form = UserCreateForm
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    return render_to_response('signup.html', {
        'form': form,
    }, RequestContext(request))


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user_authenticated = authenticate(username=username, password=password)
                if user_authenticated is not None:
                        login(request, user_authenticated)
                        return redirect('home', username)
                else:
                    try:
                        username = User.objects.get(email=username).username
                        user_authenticated = authenticate(username=username, password=password)
                        if user_authenticated is not None:
                            login(request, user_authenticated)
                            return redirect('home', username)
                    except:
                        pass
        return render_to_response('index.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        return render_to_response('login.html', {'form': form})
