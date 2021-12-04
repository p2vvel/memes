from os import stat
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase
from django.utils import timezone

from comments.models import Comment, MemeComment
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from django.conf import settings

from memes_app.models import Meme
from django.core import serializers

from django.utils import timezone

import json
# Create your tests here.


class TestCommentsFetch(TestCase):
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


    def test_comments_new(self):
        '''Tests if sorting comments works'''
        meme = Meme.objects.all()[0]
        comments_content = [
            ("Hehe :-)", None), 
            (":-|", 0), 
            ("Not hehe >:-(", 0),
            ("Marik1234, im back", None),
            ("With friends", 3),
            ("Polska gurom hehe", 3),
            ("litosci", None),
            (":(((", None),
            ]
        self.client.login(**self.new_user_data)
        comments = []
        for content, parent in comments_content:
            temp = MemeComment(
                original_poster=get_user(self.client), 
                content=content, 
                comment_object=meme,
                parent_comment= parent if parent is None else comments[parent]
                )
            temp.save()
            comments.append(temp)
        

        response = self.client.post("%s?sort=new" % reverse("get_meme_comment", args=(meme.pk,)))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual([k[0] for k in comments_content], [k["fields"]["content"] for k in data["comments"]])


    def test_comments_new_no_sort_paramater(self):
        '''Tests if sorting comments works, no sort parameter in url specified'''
        meme = Meme.objects.all()[0]
        comments_content = [
            ("Hehe :-)", None),
            (":-|", 0),
            ("Not hehe >:-(", 0),
            ("Marik1234, im back", None),
            ("With friends", 3),
            ("Polska gurom hehe", 3),
            ("litosci", None),
            (":(((", None),
            ]
        self.client.login(**self.new_user_data)
        comments = []
        for content, parent in comments_content:
            temp = MemeComment(
                original_poster=get_user(self.client), 
                content=content, 
                comment_object=meme,
                parent_comment= parent if parent is None else comments[parent]
                )
            temp.save()
            comments.append(temp)
        

        response = self.client.post("%s" % reverse("get_meme_comment", args=(meme.pk,)))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual([k[0] for k in comments_content], [k["fields"]["content"] for k in data["comments"]])


    def test_comments_best_sort(self):
        '''Tests if sorting comments works'''
        meme = Meme.objects.all()[0]
        comments_content = [
            ("Hehe :-)", None, 15),
            (":-|", 0, 240),
            ("Not hehe >:-(", 0, 3),
            ("Marik1234, im back", None, 120),
            ("With friends", 3, 3),
            ("Polska gurom hehe", 3, 20),
            ("litosci", None, -21),
            (":(((", None, 0),
            ]
        comments_sorted_content = [
            ("Marik1234, im back", None, 120),
            
            ("With friends", 3, 3),
            ("Polska gurom hehe", 3, 20),
            
            ("Hehe :-)", None, 15),
            (":-|", 0, 240),
            ("Not hehe >:-(", 0, 3),

            
            (":(((", None, 0),
            ("litosci", None, -21),
            ]

        self.client.login(**self.new_user_data)
        comments = []
        for content, parent, karma in comments_content:
            temp = MemeComment(
                original_poster=get_user(self.client), 
                content=content, 
                comment_object=meme,
                parent_comment= parent if parent is None else comments[parent],
                karma=karma,
                )
            temp.save()
            comments.append(temp)
        

        response = self.client.post("%s?sort=best" % reverse("get_meme_comment", args=(meme.pk,)))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual([k[0] for k in comments_sorted_content], [k["fields"]["content"] for k in data["comments"]])


    def test_comments_best_sort_same_karma(self):
        '''Tests if sorting comments works, comments with same amount of karma should be sorted by oldest'''
        meme = Meme.objects.all()[0]
        comments_content = [
            ("Hehe :-)", None, 0),
            (":-|", 0, 0),
            ("Not hehe >:-(", 0, 0),
            ("Marik1234, im back", None, 0),
            ("With friends", 3, 0),
            ("Polska gurom hehe", 3, 0),
            ("litosci", None, 0),
            (":(((", None, 0),
            ]

        self.client.login(**self.new_user_data)
        comments = []
        for content, parent, karma in comments_content:
            temp = MemeComment(
                original_poster=get_user(self.client), 
                content=content, 
                comment_object=meme,
                parent_comment= parent if parent is None else comments[parent],
                karma=karma,
                
                )
            temp.save()
            comments.append(temp)
        

        response = self.client.post("%s?sort=best" % reverse("get_meme_comment", args=(meme.pk,)))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual([k[0] for k in comments_content], [k["fields"]["content"] for k in data["comments"]])


    def test_comments_new_sort_same_time(self):
        '''Tests if sorting comments works, comments with same amount of karma should be sorted by oldest'''
        meme = Meme.objects.all()[0]
        comments_content = [
            ("Hehe :-)", None, 120),
            (":-|", 0, 90),
            ("Not hehe >:-(", 0, 0),

            ("Marik1234, im back", None, 360),
            ("With friends", 3, 0),
            ("Polska gurom hehe", 3, 0),

            ("litosci", None, 0),
            
            (":(((", None, 0),
        ]

        comments_sorted_content = [
            ("Marik1234, im back", None, 360),
            ("With friends", 3, 0),
            ("Polska gurom hehe", 3, 0),
            
            ("Hehe :-)", None, 120),
            (":-|", 0, 90),
            ("Not hehe >:-(", 0, 0),

            ("litosci", None, 0),
            
            (":(((", None, 0),
        ]


        self.client.login(**self.new_user_data)
        now = timezone.now()
        comments = []
        for content, parent, karma in comments_content:
            temp = MemeComment(
                original_poster=get_user(self.client), 
                content=content, 
                comment_object=meme,
                parent_comment= parent if parent is None else comments[parent],
                karma=karma,
                
                )
            temp.save()
            comments.append(temp)
        
        for k in comments:
            k.date_created = now
            k.save()
        

        response = self.client.post("%s?sort=new" % reverse("get_meme_comment", args=(meme.pk,)))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        response_data = [k[0] for k in comments_sorted_content]
        
        my_data = [k["fields"]["content"] for k in data["comments"]]
        self.assertEqual(response_data, my_data)