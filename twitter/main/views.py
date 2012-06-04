# -.- coding:utf8 -.-
from main.models import Profile, Tweet
from django.contrib.auth.models import User
from main.forms import UserForm, Log_inForm, Edit_ProfileForm, TweetForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext


def index(request):
    return render_to_response('index.html')


def sign_up(request):
    form = UserForm
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('log_in')
    return render_to_response('sign_up.html', {
        'form': form, },
        RequestContext(request))


def log_in(request):
    if request.method == 'POST':
        form = Log_inForm(request.POST)
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
        return render_to_response('index.html', {
            'form': form},
            context_instance=RequestContext(request))
    else:
        form = Log_inForm()
        return render_to_response('log_in.html', {
            'form': form, },
            RequestContext(request))


@login_required
def home(request):
    profile = request.user.get_profile()
    tweet = Tweet.objects.filter(owner=profile.pk)
    users = Profile.objects.exclude(pk=profile.pk)
    try:
        Profile.objects.get(user=request.user, follow=users)
        action = "unfollow"
    except Profile.DoesNotExist:
        action = "follow"
    return render_to_response('home.html', {
        'profile': profile,
        'tweet': tweet,
        'users': users,
        'action': action, },
        RequestContext(request))


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = Edit_ProfileForm(request.POST, instance=Profile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render_to_response('sign_up.html', {
                'form': form, },
                RequestContext(request))
    form = Edit_ProfileForm(instance=Profile.objects.get(user=request.user))
    return render_to_response('edit_profile.html', {
        'form': form, },
        RequestContext(request))


@login_required
def post_tweet(request):
    form = TweetForm()
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            owner = Profile.objects.get(user=request.user)
            Tweet.objects.create(owner=owner, status=status)
            return redirect('home')
    return render_to_response('post_tweet.html', {
        'form': form, },
        RequestContext(request))


@login_required
def edit_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    form = TweetForm(instance=tweet)
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render_to_response('post_tweet.html', {
        'form': form,
        }, RequestContext(request))


@login_required
def delete_tweet(request, pk):
    Tweet.objects.filter(pk=pk).delete()
    return redirect('home')


@login_required
def follow(request, pk):
    followed = Profile.objects.get(pk=pk)
    follower = Profile.objects.get(user=request.user)
    try:
        Profile.objects.get(user=request.user, follow=followed)
        follower.follow.remove(followed)
    except Profile.DoesNotExist:
        follower.follow.add(followed)
    return redirect('home')


@login_required
def visit_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    tweet = Tweet.objects.filter(owner=pk)
    if profile.is_public:
        public = "true"
    else:
        try:
            Profile.objects.get(user=request.user, follow=profile)
            public = "true"
        except Profile.DoesNotExist:
            public = "false"
    return render_to_response('visit_profile.html', {
        'profile': profile,
        'tweet': tweet,
        'public': public, },
        RequestContext(request))
