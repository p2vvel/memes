"""memes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.http.response import HttpResponse
from django.urls import path
from django.urls.conf import include


from django.shortcuts import render

from .models import Meme

from .views import MainMemeView, MemeView, MemeAdd, karma_change, FreshMemeView


urlpatterns = [
    #default page is 1 if not specified
    path("", MainMemeView.as_view(), name="index"),
    path("page/<int:page>/", MainMemeView.as_view(), name="memes"),
    path("fresh/", FreshMemeView.as_view(), name="fresh_index"),
    path("fresh/page/<int:page>/", FreshMemeView.as_view(), name="fresh_memes"),
    path("meme_add/", MemeAdd.as_view(), name="meme_add"),
    path("meme/<int:pk>/", MemeView.as_view(), name="meme_view"),
    path("meme/<int:pk>/karma/", karma_change, name="meme_karma_change")
]