from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    head_shot = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True)
    location = models.CharField(max_length=75, blank=True)
    biography = models.CharField(max_length=250, blank=True)
    follow = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __unicode__(self):
        return self.user.username


def get_profile(user):
    if not hasattr(user, '_profile_cache'):
        profile, created = Profile.objects.get_or_create(user=user)
        user._profile_cache = profile
    return user._profile_cache
User.get_profile = get_profile


class Tweet(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profile)
    status = models.CharField(max_length=140)
