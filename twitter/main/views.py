# -.- coding:utf8 -.-
from main.models import Profile
from django.contrib.auth.models import User
from main.forms import UserCreateForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
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
            return redirect('log_in')
    return render_to_response('sign_up.html', {'form': form, },
        RequestContext(request))


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                users = authenticate(username=username, password=password)
                if users is not None:
                        login(request, users)
                        return redirect('home')
                else:
                    try:
                        username = User.objects.get(email=username).username
                        users = authenticate(username=username, password=password)
                        if users is not None:
                            login(request, users)
                            return redirect('home')
                    except:
                        pass
        return render_to_response('index.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        dic = {'form': form}
        dic.update(csrf(request))
        return render_to_response('log_in.html', dic)


@login_required
def home(request):
    profile = request.user.get_profile()
    return render_to_response('home.html', {
        'profile': profile
        }, RequestContext(request))
