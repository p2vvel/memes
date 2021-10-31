from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from pathlib import Path

from memes_app.models import Meme




class TestMemeView(TestCase):
    def setUp(self):
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in ("avatar1.png", "avatar2.png")]
        # for k in image_paths:
        #     title = k.stem
        #     description = k.stem + "meme"
        #     original_image = SimpleUploadedFile(k.name, open(k, "rb").read())
        #     new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
        #     new_meme.save()
    
    def test_png_upload(self)