from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import request
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class LoginTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        new_user = user_model(login="jerry", email="jerry@example.com")
        new_user.set_password("1234")
        new_user.save()

    def test_login(self):
        '''Is login system working?'''
        self.assertTrue(self.client.login(email="jerry@example.com", password="1234"))

    def test_logout(self):
        '''Does logging out works?'''
        self.assertTrue(self.client.login(email="jerry@example.com", password="1234"))
        response = self.client.get(reverse("logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_password_change_view_anonymous(self):
        '''Is password change view visible for logged user?'''
        response = self.client.get(reverse("password_change"), follow=True)
        self.assertRedirects(response, expected_url="{}?next={}".format(reverse("login"), reverse("password_change")))

    def test_login_redirect(self):
        '''Logged user shouldnt be able to visit login page'''
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("index"), )