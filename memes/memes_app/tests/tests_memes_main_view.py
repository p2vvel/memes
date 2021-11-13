from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from pathlib import Path

from memes_app.models import Meme



class TestFreshView(TestCase):
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

    def test_memes_fresh_index(self):
        '''Do memes appear in fresh view?'''
        response = self.client.get(reverse("fresh_index"))
        memes = Meme.objects.all().order_by("-date_created")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["memes"], memes[:8])

    def test_memes_fresh_pagination(self):
        '''Do memes appear in fresh view?'''
        response = self.client.get(reverse("fresh_memes", args=(2,)))
        memes = Meme.objects.all().order_by("-date_created")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["memes"], memes[8:])    

    def test_memes_fresh_pagination_exclude_accepted(self):
        '''Do memes appear in fresh view?'''
        memes = Meme.objects.all().order_by("-date_created")
       
        for k in memes[:2]:
            k.accepted = True
            k.save(update_fields=["accepted"])
        
        response = self.client.get(reverse("fresh_index"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["memes"], memes[2:])

    def test_memes_fresh_check_hidden(self):
        '''Do hidden memes appear in fresh view?'''
        memes = Meme.objects.all().order_by("-date_created")

        for k in memes[5:]:
            k.hidden = True
            k.save()

        response = self.client.get(reverse("fresh_index"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(memes[:5], response.context["memes"])
        
    def test_fresh_overflow_page(self):
        '''Check what happens if someone tries to open too high page'''
        response = self.client.get(reverse("fresh_memes", args=(100,))) #trying to open 100th page

        self.assertEqual(response.status_code, 404)


    

