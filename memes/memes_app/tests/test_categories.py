from django import urls
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from pathlib import Path

from memes_app.models import Category, Meme


#Expected behaviour:
#every category has its own subpage for accepted memes (memes without category are shown on the main page)
#fresh memes are shown on common page with with builtin filter
#memes with hidden category arent shown in fresh view for anonymous users
#non-public categories are for logged users only


class TestMemeCategories(TestCase):
    def setUp(self):
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        image_names = ("avatar1.png", "avatar2.png", "cat1.jpg", "cat2.jpg", "cat3.jpg", "kiwka.gif", "meme1.jpg", "meme2.jpg", "stupki.gif", "watermark.png")

        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in image_names]
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.stem, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.save()

  
    def test_in_fresh_view(self):
        Category.objects.create(name="Paws")
        memes = Meme.objects.all()

        for k in memes:
            temp = k
            temp.accepted = True
            temp.save()

        