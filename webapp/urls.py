from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$',"Blinker.views.home", name='home'),
    url(r'^searches$',"Blinker.views.searchyelp", name='searchyelp'),
    url(r'^cleanJson$',"Blinker.views.cleanJson", name='cleanJson'),
)

