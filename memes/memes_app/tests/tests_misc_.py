from django import urls
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from pathlib import Path

from memes_app.models import Category, Meme


#Expected behaviour:
#every category has its own subpage for accepted memes (memes without category are shown on the main page)
#fresh memes are shown on common page with with builtin filter
#memes with hidden category arent shown in fresh view for anonymous users
#non-public categories are for logged users only


# class TestMemeCategories(TestCase):
#     def test_url_get_parameters(self):
#         response = self.client.get(reverse("fresh_index") + "?dupa=2&dupa=3")

#         a = 12
#         # print(response.content)
#         self.assertEqual(True, True)