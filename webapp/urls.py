from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',"Blinker.views.home", name='home'),
    url(r'^searches$',"Blinker.views.searchyelp", name='searchyelp'),
    url(r'^pointsArray$',"Blinker.views.pointsArray", name='pointsArray'),
)

