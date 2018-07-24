from django.urls import resolve
from django.http import HttpRequest
from django.test import TestCase

from homepage.views import index
from stock import views


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/stock/index/')
        self.assertEqual(found.func, views.index)