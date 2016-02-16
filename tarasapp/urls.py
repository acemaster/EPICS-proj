from django.conf.urls import include, url
from django.contrib import admin
from tarasapp.views import *

urlpatterns = [
    url(r'^testmessage/', sendmessage),
]