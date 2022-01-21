from django.urls import path

from .views import MainMemeView, MemeView, NewFreshView, MemeAdd, acceptance_change, karma_change, FreshMemeView, visibility_change


urlpatterns = [
    # default page is 1 if not specified
    path("", MainMemeView.as_view(), name="index"),
    path("page/<int:page>/", MainMemeView.as_view(), name="memes"),
    # different page only for testing new fresh view
    path("new_fresh/", NewFreshView.as_view(), name="new_fresh_index"),

    path("fresh/", FreshMemeView.as_view(), name="fresh_index"),
    path("fresh/page/<int:page>/", FreshMemeView.as_view(), name="fresh_memes"),
    path("meme_add/", MemeAdd.as_view(), name="meme_add"),
    # TODO: identifying meme by slug not pk:
    path("meme/<int:pk>/", MemeView.as_view(), name="meme_view"),
    path("meme/<int:pk>/karma/", karma_change, name="meme_karma_change"),
    path("meme/<int:pk>/visibility/", visibility_change, name="meme_visibility_change"),
    path("meme/<int:pk>/acceptance/", acceptance_change, name="meme_acceptance_change"),
]
