from django import urls
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from pathlib import Path

from memes_app.models import Meme


class TestMemeModel(TestCase):
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

    def test_model_edit_save(self):
        '''Just checking if meme object saving works'''
        memes = Meme.objects.all()
        for k in memes:
            k.accepted = True
            k.save()

        for k in Meme.objects.all():
            self.assertEqual(k.accepted, True)
    
    def test_model_edit_save2(self):
        '''Just checking if meme object saving works'''
        memes = Meme.objects.all()
        for k in range(len(memes)):
            memes[k].accepted = True
            memes[k].save()

        for k in Meme.objects.all():
            self.assertEqual(k.accepted, True)

    def test_model_edit_save3(self):
        '''Just checking if meme object saving works'''
        memes = Meme.objects.all()
        for k in range(len(memes)):
            memes[k].accepted = True
            memes[k].save()

        self.assertCountEqual([k.accepted for k in memes], [k.accepted for k in Meme.objects.all()])