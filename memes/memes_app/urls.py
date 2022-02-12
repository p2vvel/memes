from django.urls import path

from .views import MainMemeView, MemeView, FreshMemeView, MemeAdd, acceptance_change, karma_change, FreshMemeView, \
    visibility_change, CategoryView, NewMainMemeView

urlpatterns = [
    # default page is 1 if not specified
    path("", MainMemeView.as_view(), name="index"),
    path("page/<int:page>/", MainMemeView.as_view(), name="memes"),

    path("new/", NewMainMemeView.as_view(), name="new_index"),
    path("new/page/<int:page>/", NewMainMemeView.as_view(), name="new_memes"),

    path("fresh/", FreshMemeView.as_view(), name="fresh_index"),
    path("fresh/page/<int:page>/", FreshMemeView.as_view(), name="fresh_memes"),


    path("category/<slug:category>/", CategoryView.as_view(), name="category_view"),
    # path("page/<int:page>/", MainMemeView.as_view(), name="memes"),


    path("meme_add/", MemeAdd.as_view(), name="meme_add"),
    # TODO: identifying meme by slug not pk:
    path("meme/<int:pk>/", MemeView.as_view(), name="meme_view"),
    path("meme/<int:pk>/karma/", karma_change, name="meme_karma_change"),
    path("meme/<int:pk>/visibility/", visibility_change, name="meme_visibility_change"),
    path("meme/<int:pk>/acceptance/", acceptance_change, name="meme_acceptance_change"),
]
