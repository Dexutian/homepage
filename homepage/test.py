from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from homepage.views import index

class HomePageTest(TestCase):
    '''
    首页测试
    '''

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)