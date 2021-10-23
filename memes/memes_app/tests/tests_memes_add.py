from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from pathlib import Path

from memes_app.models import Meme


class TestMemesAddBase(TestCase):
    '''Tests memes model before adding resizing'''
    def setUp(self):
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()        

    def test_add_meme_anonymous(self):
        '''Anonymous user shouldnt be able to add meme'''
        img_path = settings.BASE_DIR.parent / "test_images" / "avatar1.png"

        title = "Doggo wattero mellono"
        description = "Nothing to see :))"
        img = SimpleUploadedFile(img_path.name, open(img_path, "rb").read())
        
        data = {"title": title, "description": description, "original_image": img}
        response = self.client.post(reverse("meme_add"), data=data, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(0, Meme.objects.all().count())     #meme wasnt added

    def test_add_meme_full_data(self):
        '''Does meme adding works?'''
        self.client.login(email="jerry@example.com", password="1234")
        img_path = settings.BASE_DIR.parent / "test_images" / "avatar1.png"

        title = "Doggo wattero mellono"
        description = "Nothing to see :))"
        img = SimpleUploadedFile(img_path.name, open(img_path, "rb").read())
        
        data = {"title": title, "description": description, "original_image": img}
        response = self.client.post(reverse("meme_add"), data=data, follow=True)
        added_meme = Meme.objects.get(title=title)
        self.assertRedirects(response, reverse("meme_view", args=(added_meme.pk,)))
        self.assertEqual(added_meme.title, title)
        self.assertEqual(added_meme.description, description)
        self.assertTrue(Path(added_meme.original_image.path).is_file())     #check if file was saved

    def test_add_meme_no_description(self):
        '''Does meme adding works?'''
        self.client.login(email="jerry@example.com", password="1234")
        img_path = settings.BASE_DIR.parent / "test_images" / "avatar1.png"

        title = "Doggo wattero mellono"
        img = SimpleUploadedFile(img_path.name, open(img_path, "rb").read())
        
        data = {"title": title, "original_image": img}
        response = self.client.post(reverse("meme_add"), data=data, follow=True)
        added_meme = Meme.objects.get(title=title)
        self.assertRedirects(response, reverse("meme_view", args=(added_meme.pk,)))
        self.assertEqual(added_meme.title, title)
        self.assertTrue(Path(added_meme.original_image.path).is_file())     #check if file was saved

    def test_add_meme_no_title(self):
        '''Does meme adding works?'''
        self.client.login(email="jerry@example.com", password="1234")
        img_path = settings.BASE_DIR.parent / "test_images" / "avatar1.png"

        description = "Nothing to see :))"
        img = SimpleUploadedFile(img_path.name, open(img_path, "rb").read())
        
        data = {"description": description, "original_image": img}
        response = self.client.post(reverse("meme_add"), data=data, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(0, Meme.objects.all().count())     #meme wasnt added

    def test_add_meme_no_image(self):
        '''Does meme adding works?'''
        self.client.login(email="jerry@example.com", password="1234")

        title = "Doggo wattero mellono"
        description = "Nothing to see :))"
        
        data = {"title": title, "description": description}
        response = self.client.post(reverse("meme_add"), data=data, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(0, Meme.objects.all().count())     #meme wasnt added

    def test_add_meme_form_logged(self):
        '''Does logged user can see meme add form?'''
        self.client.login(email="jerry@example.com", password="1234")
        response = self.client.get(reverse("meme_add"))
        self.assertEqual(response.status_code, 200)
    
    def test_add_meme_form_anonymous(self):
        '''Does logged user can see meme add form?'''
        response = self.client.get(reverse("meme_add"), follow=True)
        # self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "{}?next={}".format(reverse("login"), reverse("meme_add")))



