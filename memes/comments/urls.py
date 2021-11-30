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

from .views import AddMemeComment, AddReplyComment, GetMemeComments



urlpatterns = [
    #default page is 1 if not specified
    path("meme/<int:pk>/", GetMemeComments.as_view(), name="get_meme_comment"),
    path("meme/<int:pk>/add/", AddMemeComment.as_view(), name="add_meme_comment"),
    path("comment/<int:pk>/add/", AddReplyComment.as_view(), name="add_reply_comment"),
]