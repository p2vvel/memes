from django.test import TestCase

from django.http.request import QueryDict

from memes_app.templatetags.preserve_filters import preserve_filters

class TestPreserveFiltersTag(TestCase):
    def test_all_parameters(self):
        params = QueryDict()
        params._mutable = True  #QueryDict is immutable by default
        params.setlist("category", ["first", "second", "third"])
        params.setlist("sort", ["new"])
        self.assertTrue(preserve_filters("", params), "?sort=new&category=first&category=second&category=third")

    def test_only_categories(self):
        params = QueryDict()
        params._mutable = True  #QueryDict is immutable by default
        params.setlist("category", ["first", "second", "third"])
        self.assertEqual(preserve_filters("", params), "?category=first&category=second&category=third")

    def test_only_sort(self):
        params = QueryDict()
        params._mutable = True  #QueryDict is immutable by default
        params.setlist("sort", ["new"])
        self.assertEqual(preserve_filters("", params), "?sort=new")

    def test_no_parameters(self):
        params = QueryDict()
        params._mutable = True  #QueryDict is immutable by default
        self.assertEqual(preserve_filters("", params), "")

    def test_all_parameters_trash(self):
        params = QueryDict()
        params._mutable = True  #QueryDict is immutable by default
        params.setlist("category", ["first", "second", "third"])
        params.setlist("sort", ["new"])
        params.setlist("test", ["test1", "test2", "test3"])
        self.assertTrue(preserve_filters("", params), "?sort=new&category=first&category=second&category=third")

    def test_trash_parameters_only(self):
        params = QueryDict()
        params._mutable = True  #QueryDict is immutable by default
        params.setlist("test", ["test1", "test2", "test3"])
        self.assertEqual(preserve_filters("", params), "")