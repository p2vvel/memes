from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user, get_user_model
from django.test.utils import override_settings
from django.urls import reverse
from pathlib import Path

from memes_app.models import Meme


from PIL import Image


@override_settings(DEBUG=True)
class TestMemeView(TestCase):
    def setUp(self):
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        self.base_path = settings.BASE_DIR.parent / "test_images"
        self.login_data = {"email": "jerry@example.com", "password": "1234"}
        # for k in image_paths:
        #     title = k.stem
        #     description = k.stem + "meme"
        #     original_image = SimpleUploadedFile(k.name, open(k, "rb").read())
        #     new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
        #     new_meme.save()
    
    def test_png_upload(self):
        '''tests if user can send memes in .png format'''
        self.client.login(**self.login_data)
        for k in ["avatar1.png", "avatar2.png"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            new_meme.save()
            #TODO: finish tests
            self.assertTrue(Path(new_meme.original_image.path).is_file())
            img_ori = Image.open(new_meme.original_image.path)
            self.assertEqual(Path(new_meme.original_image.path).suffix, ".png")
            self.assertEqual(img_ori.format, "PNG")
            self.assertTrue(Path(new_meme.normal_image.path).is_file())
            img_nor = Image.open(new_meme.normal_image.path)
            self.assertEqual(img_nor.format, "PNG")

    def test_jpg_upload(self):
        '''tests if user can send memes in .jpg format'''
        self.client.login(**self.login_data)
        for k in ["meme1.jpg", "meme2.jpg"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            new_meme.save()
            #TODO: finish tests
            self.assertTrue(Path(new_meme.original_image.path).is_file())
            img_ori = Image.open(new_meme.original_image.path)
            self.assertEqual(Path(new_meme.original_image.path).suffix, ".jpg")
            self.assertEqual(img_ori.format, "JPEG")
            self.assertTrue(Path(new_meme.normal_image.path).is_file())
            img_nor = Image.open(new_meme.normal_image.path)
            self.assertEqual(img_nor.format, "JPEG")