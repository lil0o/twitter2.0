from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('main.views',
    url(r'^$', 'index'),
    url(r'^sign_up$', 'sign_up', name='sign_up'),
    url(r'^log_in$', 'log_in', name='log_in'),
    url(r'^home$', 'home', name='home'),
    url(r'^profile/edit/$', 'edit_profile', name='edit_profile'),
    url(r'^tweet/post/$', 'post_tweet', name='post_tweet'),
    url(r'^tweet/(?P<pk>\d+)/edit/$', 'edit_tweet', name='edit_tweet'),
    url(r'^tweet/(?P<pk>\d+)/delete/$', 'delete_tweet', name='delete_tweet'),
    url(r'^profile/(?P<pk>\d+)/$', 'show_profile', name='show_profile'),
    url(r'^follow/$', 'follow'),
)
