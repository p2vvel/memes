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
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.name, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.save()
    
    def test_karma_anonymous(self):
        '''Anonymous user shouldnt be able to change karma points state'''
        memes = Meme.objects.all()
        for m in memes:
            response = self.client.get(reverse("meme_karma_change", args=(m.pk,)), follow=True)
            self.assertRedirects(response, reverse("index"))    #anonymous user should be redirected
            m.refresh_from_db()
            self.assertEqual(0, m.karma)    #karma points should remain unchanged

    def test_karma_logged(self):
        '''Logged user should be able to give karma points to meme'''
        self.client.login(email="jerry@example.com", password="1234")
        memes = Meme.objects.all()
        meme = memes[0]
        for k in [1, 0, 1, 0]:
            response = self.client.get(reverse("meme_karma_change", args=(meme.pk,)), follow=True)
            self.assertRedirects(response, reverse("meme_view", args=(meme.pk,)))
            meme.refresh_from_db()
            self.assertEqual(meme.karma, k)

    def test_karma_404(self):
        '''Adding karma to non existing meme should raise 404'''
        self.client.login(email="jerry@example.com", password="1234")
        response = self.client.get("/meme/{pk}/karma/".format(pk=999))      #reverse was raising exception
        self.assertEqual(response.status_code, 404)
