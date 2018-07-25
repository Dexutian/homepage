from django.urls import resolve
from django.http import HttpRequest
from django.test import TestCase

from stock import views


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/stock/index/')
        self.assertEqual(found.func, views.index)

    def test_root_url_resolves_to_name_file(self):
        found = resolve('/stock/name_file/')
        self.assertEqual(found.func, views.name_file)

    def test_root_url_resolves_to_pricedaily_data(self):
        found = resolve('/stock/pricedaily_data/')
        self.assertEqual(found.func, views.pricedaily_data)