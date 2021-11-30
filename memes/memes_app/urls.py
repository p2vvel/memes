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
from django.urls import path



from .views import MainMemeView, MemeView, MemeAdd, acceptance_change, karma_change, FreshMemeView, visibility_change


urlpatterns = [
    #default page is 1 if not specified
    path("", MainMemeView.as_view(), name="index"),
    path("page/<int:page>/", MainMemeView.as_view(), name="memes"),
    path("fresh/", FreshMemeView.as_view(), name="fresh_index"),
    path("fresh/page/<int:page>/", FreshMemeView.as_view(), name="fresh_memes"),
    path("meme_add/", MemeAdd.as_view(), name="meme_add"),
    #identyfy meme by slug not pk:
    path("meme/<int:pk>/", MemeView.as_view(), name="meme_view"),
    path("meme/<int:pk>/karma/", karma_change, name="meme_karma_change"),
    path("meme/<int:pk>/visibility/", visibility_change, name="meme_visibility_change"),
    path("meme/<int:pk>/acceptance/", acceptance_change, name="meme_acceptance_change"),
]