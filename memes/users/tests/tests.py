from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


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

    