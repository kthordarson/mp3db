"""mymp3thing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from mp3db.views import hello,current_datetime,  artist_list,getalbums,getalbum_tracks,search,artist
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello, name="hello"),
    path('time', current_datetime),
    path('artist_list/', artist_list,name='artist_list'),
    path('artist/', artist,name='artist'),
    re_path(r'^getalbums/$', getalbums, name='getalbums'),
    re_path(r'^getalbum_tracks/$', getalbum_tracks, name='gettracks'),
    re_path(r'^search/$', search),
]
if settings.DEBUG:
   import debug_toolbar
   urlpatterns += [
       url(r'^__debug__/', include(debug_toolbar.urls)),
   ]
