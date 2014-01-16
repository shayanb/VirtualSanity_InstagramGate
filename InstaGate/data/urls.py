__author__ = 'sbeta'

from django.conf.urls import patterns, url

from data import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<user_id>\d+)/$', views.user, name='user'),
    url(r'^tag/(?P<tag>\w+)/$', views.tag, name='tag'),
    url(r'^media/(?P<media_id>\w+)/$', views.media, name='media'),
    url(r'^token/$', views.oauth, name='oauth'), #callback function to receive the access token
    url(r'^gettoken/$', views.getoauth, name='oauth'), # to get authenticated oAuth





#r'^(?P<question_id>\d+)/$'


    )

