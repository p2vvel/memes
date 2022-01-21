import datetime

from django.test import TestCase

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from memes_app.models import Meme, Category


class TestFreshMemeViewBase(TestCase):
    def setUp(self):
        self.new_user_data = {"email": "jerry@example.com", "password": "1234"}
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()

        Category.objects.create(name="F1")
        Category.objects.create(name="paws")
        self.categories = Category.objects.all()

        image_names = ("avatar1.png", "avatar2.png", "cat1.jpg", "cat2.jpg", "cat3.jpg", "kiwka.gif", "meme1.jpg", "meme2.jpg", "stupki.gif", "watermark.png")
        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in image_names]
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.stem, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.save()

    def test_no_category(self):
        memes = Meme.objects.all().order_by("-date_created")
        meme_ids = [k.pk for k in memes]

        response = self.client.get(reverse("new_fresh_index"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[:8], [k.pk for k in response.context["memes"]])

        response = self.client.get(reverse("new_fresh_index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[8:], [k.pk for k in response.context["memes"]])

    def test_category_fresh(self):
        """Test if meme categories works"""
        memes = Meme.objects.all().order_by("-date_created")
        meme_ids = [k.pk for k in memes]

        paws = Category.objects.get(name__iexact="paws")
        f1 = Category.objects.get(name__iexact="f1")

        for k in [0, 1, 2]:
            memes[k].category = paws
            memes[k].save()

        for k in [3, 4, 5]:
            memes[k].category = f1
            memes[k].save()

        response = self.client.get(reverse("new_fresh_index") + "?category=paws")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[:3], [k.pk for k in response.context["memes"]])

        response = self.client.get(reverse("new_fresh_index") + "?category=f1")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[3:6], [k.pk for k in response.context["memes"]])

        # test multiple categories
        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[:6], [k.pk for k in response.context["memes"]])

        # test multiple categories and memes without category
        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws&category=none")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[:8], [k.pk for k in response.context["memes"]])
        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws&category=none&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[8:], [k.pk for k in response.context["memes"]])

    def test_restricted_category_anonymous(self):
        """Test if anonymous user can see memes from private categories"""
        memes = Meme.objects.all().order_by("-date_created")
        meme_ids = [k.pk for k in memes]

        paws = Category.objects.get(name__iexact="paws")
        paws.public = False
        paws.save()
        f1 = Category.objects.get(name__iexact="f1")

        for k in [0, 1, 2]:
            memes[k].category = paws
            memes[k].save()

        for k in [3, 4, 5]:
            memes[k].category = f1
            memes[k].save()

        response = self.client.get(reverse("new_fresh_index") + "?category=paws")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([], [k.pk for k in response.context["memes"]])

        response = self.client.get(reverse("new_fresh_index") + "?category=f1")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[3:6], [k.pk for k in response.context["memes"]])

        # test multiple categories
        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[3:6], [k.pk for k in response.context["memes"]])

        # test multiple categories and memes without category
        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws&category=none")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[3:], [k.pk for k in response.context["memes"]])


    def test_restricted_category_logged(self):
        """Test if logged user can see memes from private categories"""
        memes = Meme.objects.all().order_by("-date_created")
        meme_ids = [k.pk for k in memes]

        paws = Category.objects.get(name__iexact="paws")
        f1 = Category.objects.get(name__iexact="f1")

        for k in [0, 1, 2]:
            memes[k].category = paws
            memes[k].save()

        for k in [3, 4, 5]:
            memes[k].category = f1
            memes[k].save()

        response = self.client.get(reverse("new_fresh_index") + "?category=paws")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[:3], [k.pk for k in response.context["memes"]])

        response = self.client.get(reverse("new_fresh_index") + "?category=f1")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[3:6], [k.pk for k in response.context["memes"]])

        # test multiple categories
        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[:6], [k.pk for k in response.context["memes"]])

        # test multiple categories and memes without category
        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws&category=none")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[:8], [k.pk for k in response.context["memes"]])\

        response = self.client.get(reverse("new_fresh_index") + "?category=f1&category=paws&category=none&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(meme_ids[8:], [k.pk for k in response.context["memes"]])

    def test_non_existing_category(self):
        """Non-existing category lookup should return empty memes"""
        response = self.client.get(reverse("new_fresh_index") + "?category=paws")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([], [k.pk for k in response.context["memes"]])




class TestFreshMemeViewSort(TestCase):
    def setUp(self):
        self.new_user_data = {"email": "jerry@example.com", "password": "1234"}
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()

        Category.objects.create(name="F1")
        Category.objects.create(name="paws")
        self.categories = Category.objects.all()

        image_names = ("avatar1.png", "avatar2.png", "cat1.jpg", "cat2.jpg", "cat3.jpg", "kiwka.gif", "meme1.jpg", "meme2.jpg", "stupki.gif", "watermark.png")
        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in image_names]
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.stem, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.save()

    def check_basic_sort(self):
        """Check if memes are sorted by newest by default"""
        memes = Meme.objects.all().order_by("-date_created")
        meme_ids = [k.pk for k  in memes]

        # test multiple categories and memes without category
        response = self.client.get(reverse("new_fresh_index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meme_ids[:8], [k.pk for k in response.context["memes"]])\

        response = self.client.get(reverse("new_fresh_index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meme_ids[8:], [k.pk for k in response.context["memes"]])

    def check_basic_sort_best(self):
        """Check if sorting memes by karma works"""
        memes = Meme.objects.all()
        for m in memes:
            m.karma = m.pk*10
            m.save()

        meme_ids = [k.pk for k in memes.order_by("-karma")]

        # test multiple categories and memes without category
        response = self.client.get(reverse("new_fresh_index") + "?sort=best")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meme_ids[:8], [k.pk for k in response.context["memes"]])

        response = self.client.get(reverse("new_fresh_index") + "?sort=best&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meme_ids[8:], [k.pk for k in response.context["memes"]])

    def check_basic_sort_best_12h(self):
        """Check if sorting memes from last 12h by karma works"""
        memes = Meme.objects.all().order_by("-pk")
        for m in memes:
            m.karma = m.pk*10
            m.save()

        for m in memes[:2]:
            m.date_created = datetime.datetime.now() - datetime.timedelta(hours=20)
            m.save()

        meme_ids = [k.pk for k in memes.order_by("-karma")]

        # test multiple categories and memes without category
        response = self.client.get(reverse("new_fresh_index") + "?sort=best12")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meme_ids[2:], [k.pk for k in response.context["memes"]])

        response = self.client.get(reverse("new_fresh_index") + "?sort=best12&page=2")
        self.assertEqual(response.status_code, 404)     # will raise 404 because there won't be any more memes to show

    def check_basic_sort_best_72h(self):
        """Check if sorting memes from last 72h by karma works"""
        memes = Meme.objects.all().order_by("-pk")
        for m in memes:
            m.karma = m.pk*10
            m.save()

        for m in memes[:2]:
            m.date_created = datetime.datetime.now() - datetime.timedelta(hours=73)
            m.save()

        for m in memes[2:4]:
            m.date_created = datetime.datetime.now() - datetime.timedelta(hours=20)
            m.save()

        meme_ids = [k.pk for k in memes.order_by("-karma")]

        # test multiple categories and memes without category
        response = self.client.get(reverse("new_fresh_index") + "?sort=best72")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meme_ids[2:], [k.pk for k in response.context["memes"]])

        response = self.client.get(reverse("new_fresh_index") + "?sort=best72&page=2")
        self.assertEqual(response.status_code, 404)     # will raise 404 because there won't be any more memes to show
