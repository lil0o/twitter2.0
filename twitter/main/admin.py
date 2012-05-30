from main.models import Profile, Tweet
from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user','head_shot', 'birth_date', 'location', 'biography')


class TweetAdmin(admin.ModelAdmin):
    model = Tweet
    list_display = ('creation_date', 'status', 'owner')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tweet, TweetAdmin)
