import datetime

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from memes_app.models import Category, Meme
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


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
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user, accepted=True)
            new_meme.save()


class TestCategoriesView(TestCase):
    setUp = setUp

    def test_category_view(self):
        """Does category view even work?"""
        for k in Category.objects.all():
            response = self.client.get(reverse("category_view", args=(k.slug,)))
            self.assertEqual(response.status_code, 200)

    def test_category_view_anonymous(self):
        """Does anonymous user can open hidden categories?"""
        categories = Category.objects.all()
        for c in categories:
            c.public = False
            c.save()

        for k in Category.objects.all():
            response = self.client.get(reverse("category_view", args=(k.slug,)))
            self.assertEqual(response.status_code, 404)

    def test_category_view_logged(self):
        """Logged user can see every existing category"""
        self.client.login(**self.new_user_data)
        memes = Meme.objects.all().order_by("-date_created")
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all()
        paws.public = False
        for m in memes[:5]:
            temp = m
            temp.category = paws
            temp.save()
        for m in memes[5:]:
            temp = m
            temp.category = f1
            temp.save()

        response = self.client.get(reverse("category_view", args=(paws.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([k.pk for k in response.context["memes"]], memes_id[:5])

        response = self.client.get(reverse("category_view", args=(f1.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([k.pk for k in response.context["memes"]], memes_id[5:])

    def test_category_bad_slug(self):
        """Bad category in url should raise 404"""
        response = self.client.get(reverse("category_view", args=("eminem",)))
        self.assertEqual(response.status_code, 404)

    def test_category_memes(self):
        """Memes appear in right category?"""
        memes = Meme.objects.all()
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all().order_by("pk");
        for m in memes:
            temp = m
            temp.category = paws
            temp.save()
        response = self.client.get(reverse("category_view", args=(paws.slug,)))
        self.assertCountEqual([k.pk for k in response.context["memes"]], memes_id[:8])
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([k.pk for k in response.context["memes"]], memes_id[8:])

    def test_category_unaccepted(self):
        """Unaccepted memes shouldn't appear in categories view, they should remain in 'fresh' view"""
        self.client.login(**self.new_user_data)
        memes = Meme.objects.all().order_by("-date_created")
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all()
        paws.public = False
        for m in memes[:5]:
            temp = m
            temp.accepted = False
            temp.category = paws
            temp.save()
        for m in memes[5:]:
            temp = m
            temp.accepted = False
            temp.category = f1
            temp.save()

        response = self.client.get(reverse("category_view", args=(paws.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([k.pk for k in response.context["memes"]], [])

        response = self.client.get(reverse("category_view", args=(f1.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual([k.pk for k in response.context["memes"]], [])


class TestCategoriesViewSort(TestCase):
    setUp = setUp

    def test_sorting_new_default(self):
        """Default sort method should be sorting by newest(using acceptance date, NOT creation date)"""
        memes = Meme.objects.all().order_by("-date_created")
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all()
        for h, m in enumerate(memes):
            temp = m
            temp.category = paws
            temp.date_accepted = timezone.now() - datetime.timedelta(hours=h)
            temp.save()

        response = self.client.get(reverse("category_view", args=(paws.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[:8])

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[8:])

    def test_sorting_new(self):
        """All memes from certain category should be sorted by karma (bigger karma first)"""
        memes = Meme.objects.all().order_by("date_created")
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all()
        for h, m in enumerate(memes):
            temp = m
            temp.category = paws
            temp.date_accepted = timezone.now() - datetime.timedelta(hours=h)
            temp.save()

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?sort=new')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[:8])

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?page=2&sort=new')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[8:])

    def test_sorting_best(self):
        """All memes from certain category should be sorted by karma (bigger karma first)"""
        memes = Meme.objects.all().order_by("date_created")
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all()
        for k, m in enumerate(memes):
            temp = m
            temp.category = paws
            temp.karma = 100 - k
            temp.save()

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?sort=best')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[:8])

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?page=2&sort=best')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[8:])

    def test_sorting_best_12h(self):
        """Memes from certain category, accepted in last 12h, should be sorted by karma (bigger karma first)"""
        memes = Meme.objects.all().order_by("date_created")
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all()

        for m in memes[:3]:
            temp = m
            temp.date_accepted = timezone.now() - datetime.timedelta(hours=13)  #outside time boundary
            temp.save()

        for m in memes[3:]:
            temp = m
            temp.date_accepted = timezone.now()
            temp.save()

        for k, m in enumerate(memes):
            temp = m
            temp.category = paws
            temp.karma = 100 - k
            temp.save()

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?sort=best12')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[3:])

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?page=2&sort=best12')
        self.assertEqual(response.status_code, 404)


    def test_sorting_best_72h(self):
        """Memes from certain category, accepted in last 72h, should be sorted by karma (bigger karma first)"""
        memes = Meme.objects.all().order_by("date_created")
        memes_id = [k.pk for k in memes]
        f1, paws = Category.objects.all()

        for m in memes[:3]:
            temp = m
            temp.date_accepted = timezone.now() - datetime.timedelta(days=3)  #outside time boundary
            temp.save()

        for m in memes[3:]:
            temp = m
            temp.date_accepted = timezone.now()
            temp.save()

        for k, m in enumerate(memes):
            temp = m
            temp.category = paws
            temp.karma = 100 - k
            temp.save()

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?sort=best72')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([k.pk for k in response.context["memes"]], memes_id[3:])

        response = self.client.get(f'{reverse("category_view", args=(paws.slug,))}?page=2&sort=best72')
        self.assertEqual(response.status_code, 404)

