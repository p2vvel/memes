from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from pathlib import Path

from memes_app.models import Meme
from django.utils import timezone


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
            new_meme.accepted = True
            new_meme.date_accepted = timezone.now()
            new_meme.save()

    def test_index_view(self):
        '''Does main view work?'''
        memes = Meme.objects.all().order_by("-date_accepted")

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(memes[:8], response.context["memes"])

    def test_memes_view_pagination(self):
        '''Does main view work?'''
        memes = Meme.objects.all().order_by("-date_accepted")
        
        response = self.client.get(reverse("memes", args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(memes[8:], response.context["memes"])

    def test_memes_view_page_overflow(self):
        '''What happens if user tries to open too high page?'''
        memes = Meme.objects.all().order_by("-date_accepted")

        response = self.client.get(reverse("memes", args=(100,)))   #trying to open 100th page
        self.assertEqual(response.status_code, 404)
        
    def test_hidden_memes(self):
        '''Hidden memes should disappear from main view(from fresh view too)'''
        memes = Meme.objects.all().order_by("-date_accepted")
        for k in memes[:2]:
            k.hidden = True
            k.save()

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["memes"], memes[2:])

    def test_unaccepted_memes(self):
        '''Memes that are not accepted shouldnt appear in main memes view'''
        memes = Meme.objects.all().order_by("-date_accepted")
        for k in memes[:4]:
            k.accepted = False
            k.save()
        
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["memes"], memes[4:])
