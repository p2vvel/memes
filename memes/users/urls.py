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
from django.http.response import HttpResponse
from django.urls import path
from django.urls.conf import include
from .views import UserProfileView, my_profile, signup_view

# app_name = "users"    #problem with redirections with default auth views when app_name is set


urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("profile/", my_profile, name="my_profile"),
    # path("profile/", UserProfileView.as_view(), "user_profile"),
    path("", include("django.contrib.auth.urls")),
]
