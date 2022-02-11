from os import stat
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from comments.models import Comment, MemeComment
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from django.conf import settings

from memes_app.models import Meme
# Create your tests here.


class TestCommentsAdd(TestCase):
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
    
    def test_anonymous_comment(self):
        '''Anonymous user is not allowed to add comment'''
        comment = "Test comment"
        meme = Meme.objects.get(pk=1)
        response = self.client.post(reverse("add_meme_comment", args=(meme.pk,)), {"content": comment})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": False, "msg": "No permission"})
        self.assertEqual(0, MemeComment.objects.all().count())
    
    def test_logged_user_comment(self):
        '''Logged user is able to add comment'''
        self.client.login(**self.new_user_data)
        comment = "Test comment"
        memes = Meme.objects.all()
        for k, m in enumerate(memes):
            response = self.client.post(reverse("add_meme_comment", args=(m.pk,)), {"content": "Meme comment %s" % k})
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"success": True, "msg": "Successfully added new comment"})
            self.assertEqual(k + 1, MemeComment.objects.all().count())
            comment = MemeComment.objects.get(comment_object=m.pk)
            self.assertEqual(comment.content, "Meme comment %s" % k)
            self.assertEqual(comment.karma, 0)
            self.assertEqual(comment.original_poster, get_user(self.client))
            self.assertEqual(comment.hidden, False)
    
    def test_empty_comment(self):
        '''User shouldnt be able to add empy comment'''
        self.client.login(**self.new_user_data)
        comment = "Test comment"
        memes = Meme.objects.all()
        for k, m in enumerate(memes):
            response = self.client.post(reverse("add_meme_comment", args=(m.pk,)), {"content": ""})
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"success": False, "msg": "Failed adding comment"})
            self.assertEqual(0, MemeComment.objects.all().count())


class TestReplyCommentAdd(TestCase):
    def setUp(self):
        self.new_user_data = {"email": "jerry@example.com", "password": "1234"}
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()
        image_names = ("cat1.jpg",)

        image_paths = [settings.BASE_DIR.parent / "test_images" / k for k in image_names]
        for k in image_paths:
            title = k.stem
            description = k.stem + "meme"
            original_image = SimpleUploadedFile(k.stem, open(k, "rb").read())
            new_meme = Meme(title=title, description=description, original_image=original_image, original_poster=new_user)
            new_meme.accepted = True
            new_meme.date_accepted = timezone.now()
            new_meme.save()
        
        meme = Meme.objects.all()[0]
        for k in ("Test comment 1", "Test comment 2"):
            comment = MemeComment(content=k, original_poster = new_user, comment_object=meme)
            comment.save()

    def test_reply_comments_anonymous(self):
        '''Anonymous user shouldnt be able to reply for a comment'''
        parent_comment = MemeComment.objects.all()[0]
        meme = Meme.objects.all()[0]

        comments_counter = MemeComment.objects.all().count()
        content = "Test reply comment"
        response = self.client.post(reverse("add_reply_comment", args=(parent_comment.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": False, "msg": "No permission"})
        self.assertEqual(MemeComment.objects.all().count(), comments_counter)


    def test_reply_comment_logged(self):
        '''Logged user should be able to reply for a comment'''
        self.client.login(**self.new_user_data)
        comments = MemeComment.objects.all()

        for k, c in enumerate(comments):
            response = self.client.post(reverse("add_reply_comment", args=(c.pk,)), {"content": "Reply comment %s :)" % k})
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"success": True, "msg": "Successfully added new comment"})
            new_comment = MemeComment.objects.all().order_by("-date_created")[0]
            self.assertEqual(new_comment.content, "Reply comment %s :)" % k)
            self.assertEqual(new_comment.original_poster, get_user(self.client))
            self.assertEqual(new_comment.parent_comment, c)
            self.assertEqual(new_comment.comment_object, c.comment_object)


    def test_reply_comment_empty(self):
        '''Logged user shouldnt be able to add empty reply comment'''
        self.client.login(**self.new_user_data)
        comments = MemeComment.objects.all()

        for k, c in enumerate(comments):
            response = self.client.post(reverse("add_reply_comment", args=(c.pk,)), {"content": ""})
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"success": False, "msg": "Failed adding comment"})
            

    def test_multi_level_replying(self):
        '''I dont want too big replying depth, so comment replying to another replying comment should have first comment as parent'''
        self.client.login(**self.new_user_data)

        comment = MemeComment.objects.all()[0]
        comments = [comment,]
        for k in range(6):
            response = self.client.post(reverse("add_reply_comment", args=(comments[-1].pk, )), {"content": "First level"})
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {"success": True, "msg": "Successfully added new comment"})
            comments.append(MemeComment.objects.all().order_by("-date_created")[0])
            self.assertEqual(comments[-1].parent_comment, comment)

        
        
