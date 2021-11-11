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

from django.core.exceptions import ValidationError
 

@override_settings(DEBUG=True)
class TestUploadFormatCorrectExtensions(TestCase):
    def setUp(self):
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        self.base_path = settings.BASE_DIR.parent / "test_images" / "wrong_extensions"
        self.login_data = {"email": "jerry@example.com", "password": "1234"}

    
    def test_upload_png_wrong_extension(self):
        '''Test uploading PNG with .wrong extensions'''
        self.client.login(**self.login_data)
        for k in ["png_avatar1.gif", "png_avatar1.html", "png_avatar2.jpg", 
                "png_avatar2.zip", "png_watermark.jpg", "png_watermark.xlss"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path /"png_format" / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            new_meme.save()
            self.assertTrue(Path(new_meme.original_image.path).is_file())
            img_ori = Image.open(new_meme.original_image.path)
            self.assertEqual(Path(new_meme.original_image.path).suffix, ".png")
            self.assertEqual(img_ori.format, "PNG")
            self.assertTrue(Path(new_meme.normal_image.path).is_file())
            img_nor = Image.open(new_meme.normal_image.path)
            self.assertEqual(img_nor.format, "PNG")

    
    def test_upload_jpeg_wrong_extension(self):
        '''Test uploading JPEG with wrong extensions'''
        self.client.login(**self.login_data)
        for k in ["jpg_cat1.php", "jpg_cat1.png", "jpg_cat2.gif", 
                    "jpg_cat2.pdf", "jpg_cat3.png", "jpg_cat3.rar"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path /"jpg_format" / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            new_meme.save()
            self.assertTrue(Path(new_meme.original_image.path).is_file())
            img_ori = Image.open(new_meme.original_image.path)
            self.assertEqual(Path(new_meme.original_image.path).suffix, ".jpg")
            self.assertEqual(img_ori.format, "JPEG")
            self.assertTrue(Path(new_meme.normal_image.path).is_file())
            img_nor = Image.open(new_meme.normal_image.path)
            self.assertEqual(img_nor.format, "JPEG")

    
    def test_upload_gif_wrong_extension(self):
        '''Test uploading GIF with wrong extensions'''
        self.client.login(**self.login_data)
        for k in ["gif_kiwka.exe", "gif_kiwka.jpg", "gif_kiwka.pdf", "gif_kiwka.png",
                "gif_stupki.docx", "gif_stupki.jpg", "gif_stupki.png", "gif_stupki.zip"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path / "gif_format" / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            new_meme.save()
            self.assertTrue(Path(new_meme.original_image.path).is_file())
            img_ori = Image.open(new_meme.original_image.path)
            self.assertEqual(Path(new_meme.original_image.path).suffix, ".gif")
            self.assertEqual(img_ori.format, "GIF")
            self.assertTrue(Path(new_meme.normal_image.path).is_file())
            img_nor = Image.open(new_meme.normal_image.path)
            self.assertEqual(img_nor.format, "GIF")

    def test_fake_png(self):
        '''Test uploading non-PNG files(different than GIF and JPEG) with .png extensions'''
        self.client.login(**self.login_data)
        for k in ["bmp_klawier_cat.png", "docx_hello_world.png", "pdf_hello_world.png", "tiff_sample_tiff.png", "webp_sample_webp.png"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path / "png_fake" / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            with self.assertRaises(ValidationError):
                new_meme.save()

    def test_fake_jpg(self):
        '''Test uploading non-JPEG files(different than GIF and PNG) with .jpg extensions'''
        self.client.login(**self.login_data)
        for k in ["bmp_klawier_cat.jpg", "docx_hello_world.jpg", "pdf_hello_world.jpg", "tiff_sample_tiff.jpg", "webp_sample_webp.jpg"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path / "jpg_fake" / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            with self.assertRaises(ValidationError):
                new_meme.save()

    def test_fake_gif(self):
        '''Test uploading non-GIF files(different than JPEG and PNG) with .gif extensions'''
        self.client.login(**self.login_data)
        for k in ["bmp_klawier_cat.gif", "docx_hello_world.gif", "pdf_hello_world.gif", "tiff_sample_tiff.gif", "webp_sample_webp.gif"]:
            title = Path(k).stem
            original_image = SimpleUploadedFile(k, open(self.base_path / "gif_fake" / k, "rb").read())
            new_meme = Meme(title=title, original_image=original_image, original_poster=get_user(self.client))
            with self.assertRaises(ValidationError):
                new_meme.save()
