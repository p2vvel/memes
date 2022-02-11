from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.utils import timezone
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
        """Just checking if meme object saving works"""
        memes = Meme.objects.all()
        for k in memes:
            k.accepted = True
            k.save()

        for k in Meme.objects.all():
            self.assertEqual(k.accepted, True)
    
    def test_model_edit_save2(self):
        """Just checking if meme object saving works"""
        memes = Meme.objects.all()
        for k in range(len(memes)):
            memes[k].accepted = True
            memes[k].save()

        for k in Meme.objects.all():
            self.assertEqual(k.accepted, True)

    def test_model_edit_save3(self):
        """Just checking if meme object saving works"""
        memes = Meme.objects.all()
        for k in range(len(memes)):
            memes[k].accepted = True
            memes[k].save()

        self.assertCountEqual([k.accepted for k in memes], [k.accepted for k in Meme.objects.all()])


class TestMemeModelVisibilityChange(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user_data = {"email": "jerry@example.com", "password": "1234"}
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        
        self.superuser_data = {"email": "delilah@example.com", "password": "1234"}
        new_superuser = user_model(login="delilah", email="delilah@example.com", is_superuser=True)
        new_superuser.set_password("1234")
        new_superuser.save()

        image_names = ("meme1.jpg", "meme2.jpg")

        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in image_names]
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.stem, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.date_accepted = timezone.now()
            new_meme.save()


    def test_visibility_change_superuser(self):
        """Check if superuser can change visibility"""
        self.client.login(**self.superuser_data)

        messages = ["Successfully hidden meme", "Successfully set meme visible"]
        memes = Meme.objects.all()
        for m in memes:
            self.assertEqual(m.hidden, False)
            
            response = self.client.post(reverse("meme_visibility_change", args=(m.pk,)), follow=True)
            m.refresh_from_db()
            self.assertJSONEqual(response.content, {"success": True, "msg": messages[1], "hidden": m.hidden})
            self.assertEqual(m.hidden, True)
            
            response = self.client.post(reverse("meme_visibility_change", args=(m.pk,)), follow=True)
            m.refresh_from_db()
            self.assertJSONEqual(response.content, {"success": True, "msg": messages[0], "hidden": m.hidden})
            self.assertEqual(m.hidden, False)


    def test_visibility_change_normal_user(self):
        """Check if normal can change visibility"""
        self.client.login(**self.user_data)

        memes = Meme.objects.all()
        for m in memes:
            self.assertEqual(m.hidden, False)
            response = self.client.post(reverse("meme_visibility_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})

            m.refresh_from_db()
            self.assertEqual(m.hidden, False)
            response = self.client.post(reverse("meme_visibility_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})
            m.refresh_from_db()
            self.assertEqual(m.hidden, False)


    def test_visibility_change_anonymous(self):
        """Check if anonymous can change visibility"""

        memes = Meme.objects.all()
        for m in memes:
            self.assertEqual(m.hidden, False)

            response = self.client.post(reverse("meme_visibility_change", args=(m.pk,)), follow=True)
            m.refresh_from_db()
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})
            self.assertEqual(m.hidden, False)

            response = self.client.post(reverse("meme_visibility_change", args=(m.pk,)), follow=True)
            m.refresh_from_db()
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})
            self.assertEqual(m.hidden, False)


    
class TestMemeModelAcceptanceChange(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user_data = {"email": "jerry@example.com", "password": "1234"}
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        
        self.superuser_data = {"email": "delilah@example.com", "password": "1234"}
        new_superuser = user_model(login="delilah", email="delilah@example.com", is_superuser=True)
        new_superuser.set_password("1234")
        new_superuser.save()

        image_names = ("meme1.jpg", "meme2.jpg")

        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in image_names]
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.stem, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.save()

    def test_acceptance_change_superuser(self):
        """Check if superuser can change acceptance"""
        self.client.login(**self.superuser_data)

        messages = ["Successfully reversed meme acceptance", "Successfully accepted meme"]
        memes = Meme.objects.all()
        for m in memes:
            self.assertEqual(m.accepted, False)
            self.assertEqual(m.date_accepted, None)
            
            response = self.client.post(reverse("meme_acceptance_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": True, "msg": messages[1], "accepted": True})
            m.refresh_from_db()
            self.assertEqual(m.accepted, True)
            
            response = self.client.post(reverse("meme_acceptance_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": True, "msg": messages[0], "accepted": False})
            m.refresh_from_db()
            self.assertEqual(m.accepted, False)

    def test_acceptance_change_normal_user(self):
        """Check if normal can change acceptance"""
        self.client.login(**self.user_data)

        memes = Meme.objects.all()
        for m in memes:
            self.assertEqual(m.accepted, False)
            self.assertEqual(m.date_accepted, None)

            response = self.client.post(reverse("meme_acceptance_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})
            m.refresh_from_db()
            self.assertEqual(m.accepted, False)
            self.assertEqual(m.date_accepted, None)


            response = self.client.post(reverse("meme_acceptance_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})
            m.refresh_from_db()
            self.assertEqual(m.accepted, False)
            self.assertEqual(m.date_accepted, None)



    def test_acceptance_change_anonymous_user(self):
        """Check if anonymous can change acceptance"""
        memes = Meme.objects.all()
        for m in memes:
            self.assertEqual(m.accepted, False)
            self.assertEqual(m.date_accepted, None)
            
            response = self.client.post(reverse("meme_acceptance_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})
            m.refresh_from_db()
            self.assertEqual(m.accepted, False)
            self.assertEqual(m.date_accepted, None)

            response = self.client.post(reverse("meme_acceptance_change", args=(m.pk,)), follow=True)
            self.assertJSONEqual(response.content, {"success": False, "msg": "No permission!"})
            m.refresh_from_db()
            self.assertEqual(m.accepted, False)
            self.assertEqual(m.date_accepted, None)


    