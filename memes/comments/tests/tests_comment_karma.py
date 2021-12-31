from os import stat
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import request
from django.test import TestCase
from django.utils import timezone

from comments.models import Comment, MemeComment
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from django.conf import settings

from memes_app.models import Meme
# Create your tests here.



class TestCommentKarma(TestCase):
    def setUp(self):
        self.new_user_data = {"email": "jerry@example.com", "password": "1234"}
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        image_names = ("cat1.jpg", "cat2.jpg", "cat3.jpg")

        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in image_names]
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.stem, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.accepted = True
            new_meme.date_accepted = timezone.now()
            new_meme.save()

    def test_comment_karma_positive(self):
        '''Tests if positive comment karma works as expected'''
        self.client.login(**self.new_user_data)
        meme = Meme.objects.all()[0]
        comment = MemeComment.objects.create(content="Hihi :)))", original_poster=get_user(self.client), comment_object=meme)

    
        for k in [1, 0, 1, 0]:
            response = self.client.post(reverse("comment_karma_change", args=(comment.pk,)), {"positive": True})
            self.assertJSONEqual(response.content, {"success": True, "karma_given": k, "karma": k, "msg": "Succesfully changed karma!"})
            comment.refresh_from_db()
            self.assertEqual(k, comment.karma)

    def test_comment_karma_negative(self):
        '''Tests if negative comment karma works as expected'''
        self.client.login(**self.new_user_data)
        meme = Meme.objects.all()[0]
        comment = MemeComment.objects.create(content="Hihi :)))", original_poster=get_user(self.client), comment_object=meme)

        for k in [-1, 0, -1, 0]:
            response = self.client.post(reverse("comment_karma_change", args=(comment.pk,)), {"positive": False})
            self.assertJSONEqual(response.content, {"success": True, "karma_given": k, "karma": k, "msg": "Succesfully changed karma!"})
            comment.refresh_from_db()
            self.assertEqual(k, comment.karma)


    def test_comment_karma_mixed(self):
        '''Tests if mixed comment karma works as expected'''
        self.client.login(**self.new_user_data)
        meme = Meme.objects.all()[0]
        comment = MemeComment.objects.create(content="Hihi :)))", original_poster=get_user(self.client), comment_object=meme)

        
        
        for k in [1, -1, 1, -1]:
            response = self.client.post(reverse("comment_karma_change", args=(comment.pk,)), {"positive": False if k==-1 else True})
            self.assertJSONEqual(response.content, {"success": True, "karma_given": k, "karma": k, "msg": "Succesfully changed karma!"})
            comment.refresh_from_db()
            self.assertEqual(k, comment.karma)

    def test_comment_karma_mixed_extended(self):
        '''Tests if mixed comment karma works as expected v2'''
        self.client.login(**self.new_user_data)
        meme = Meme.objects.all()[0]
        comment = MemeComment.objects.create(content="Hihi :)))", original_poster=get_user(self.client), comment_object=meme)
        comment.refresh_from_db()
        
        
        for p, k in zip([True, False, True, False, False, True, True, False, False], [1, -1, 1, -1, 0, 1, 0, -1, 0]):
            response = self.client.post(reverse("comment_karma_change", args=(comment.pk,)), {"positive": p})
            self.assertJSONEqual(response.content, {"success": True, "karma_given": k, "karma": k, "msg": "Succesfully changed karma!"})
            comment.refresh_from_db()
            self.assertEqual(k, comment.karma)

