from django.contrib.auth import get_user, get_user_model
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from django.core.files import File
# Create your tests here.

from pathlib import Path

class UserTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()

    def test_login(self):
        '''Is login system working?'''
        self.assertTrue(self.client.login(email="jerry@example.com", password="1234"))

    def test_login_view(self):
        '''Does login view work'''
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        '''Does logging out works?'''
        self.assertTrue(self.client.login(email="jerry@example.com", password="1234"))
        response = self.client.get(reverse("logout"))
        user = get_user(self.client)
        self.assertRedirects(response, reverse("index"))    #checks redirect after logout
        self.assertFalse(user.is_authenticated)

    def test_password_change_view_anonymous(self):
        '''Is password change view visible for logged user?'''
        response = self.client.get(reverse("password_change"), follow=True)
        self.assertRedirects(response, expected_url="{}?next={}".format(reverse("login"), reverse("password_change")))

    def test_password_change_view_logged(self):
        '''Does signed in user see password change view?'''
        self.client.login(email="jerry@example.com", password="1234")
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, 200)

    def test_login_redirect(self):
        '''Logged user shouldnt be able to visit login page'''
        self.client.login(email="jerry@example.com", password="1234")
        response = self.client.get(reverse("login"), follow=True)
        self.assertRedirects(response, expected_url=reverse("my_profile"))

    def test_profile_edit_view(self):
        '''Does logged user see edit profile page?'''
        self.client.login(email="jerry@example.com", password="1234")
        response = self.client.get(reverse("profile_edit"))
        self.assertEqual(response.status_code, 200)
    
    def test_profile_edit_anonymous(self):
        '''Test if anonymous user is redirected if trying to see profile edit view'''
        response = self.client.get(reverse("profile_edit"), follow=True)
        self.assertRedirects(response, "{}?next={}".format(reverse("login"), reverse("profile_edit")))

    def test_profile_edit_form(self):
        self.client.login(email="jerry@example.com", password="1234")
        avatar_path = Path(settings.BASE_DIR.parent, "test_images", "avatar1.png")
        
        description = "Glifosat"
        img = SimpleUploadedFile(
                avatar_path.name, 
                open(avatar_path, "rb").read()
                )

        request = self.client.post(reverse("profile_edit"), data={
                "description": description, 
                "profile_img": img
                })

        user = get_user(self.client)
        self.assertEqual(user.description, "Glifosat")  #checks description
        self.assertTrue(Path(user.profile_img.path).is_file())  #checks if avatar was saved on disk
        # response = self.client.get(user.profile_img.url)
        # self.assertEqual(response.status_code, 200) #cant test in dev env, because during all tests DEBUG variable is set to False regardless its primary value
        Path(user.profile_img.path).unlink()    #delete saved avatar after tests