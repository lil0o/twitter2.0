from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('main.views',
    url(r'^$', 'index'),
    url(r'^sign_up$', 'sign_up'),
)
