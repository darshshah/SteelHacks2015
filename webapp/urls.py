from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',"Blinker.views.home", name='home'),
    url(r'^getPlace$',"Blinker.views.searchyelp", name='getPlace'),
    url(r'^pointsArray$',"Blinker.views.pointsArray", name='pointsArray'),

)

