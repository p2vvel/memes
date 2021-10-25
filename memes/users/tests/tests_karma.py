from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.



class TestKarmaSystem(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()
        jerry = user_model(login="jerry", email="jerry@example.com")
        jerry.set_password("1234")
        jerry.save()
        delilah = user_model(login="delilah", email="delilah@example.com")
        delilah.set_password("1234")
        delilah.save()


    def test_karma_anonymous(self):
        '''Anonymous user should be redirected to index page'''
        # self.client.login(email="jerry@example.com", password="1234")
        jerry = get_user_model().objects.get(email="jerry@example.com")
        response = self.client.get(reverse("user_karma_change", args=(jerry.login,)), follow=True)
        self.assertRedirects(response, reverse("index"))

    def test_karma_change(self):
        '''User should be able to add respect point to another user'''
        jerry = get_user_model().objects.get(login="jerry")
        delilah = get_user_model().objects.get(login="delilah")
        self.client.login(email="jerry@example.com", password="1234")
        self.assertEqual(jerry.karma, 0)
        self.assertEqual(delilah.karma, 0)
        for k in [1, 0, 1, 0]:
            response = self.client.get(reverse("user_karma_change", args=(delilah.login,)), follow=True)
            self.assertRedirects(response, reverse("profile", args=(delilah.login,)))
            delilah.refresh_from_db()
            self.assertEqual(delilah.karma, k)

    def test_karma_reverse(self):
        '''User should be able to give karma to each other'''
        jerry = get_user_model().objects.get(login="jerry")
        delilah = get_user_model().objects.get(login="delilah")
        jerry.karma = 0
        jerry.save()
        delilah.karma = 0
        delilah.save()
        for x, y in zip([1, 0, 1, 0], [1, 0, 1, 0]):
            self.client.login(email="jerry@example.com", password="1234")
            response = self.client.get(reverse("user_karma_change", args=(delilah.login,)), follow=True)
            self.assertRedirects(response, reverse("profile", args=(delilah.login,)))
            delilah.refresh_from_db()
            self.assertEqual(delilah.karma, x)
            self.client.logout()

            self.client.login(email="delilah@example.com", password="1234")
            response = self.client.get(reverse("user_karma_change", args=(jerry.login,)), follow=True)
            self.assertRedirects(response, reverse("profile", args=(jerry.login,)))
            jerry.refresh_from_db()
            self.assertEqual(jerry.karma, y)
            self.client.logout()

    def test_karma_self(self):
        '''User shouldnt be able to give karma itself'''
        jerry = get_user_model().objects.get(login="jerry")
        self.client.login(email="jerry@example.com", password="1234")
        response = self.client.get(reverse("user_karma_change", args=(jerry.login,)), follow=True)
        self.assertRedirects(response, reverse("index"))
        jerry.refresh_from_db()
        self.assertEqual(jerry.karma, 0)

    def test_karma_404(self):
        '''No karma for not existing user'''
        self.client.login(email="jerry@example.com", password="1234")
        response = self.client.get(reverse("user_karma_change", args=("jules", )))
        self.assertEqual(response.status_code, 404)