from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
from blog.models import Blog

class BlogpostListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='phodal', email='h@phodal.com', password='phodal')

    def test_blog_list_page(self):
        Blog.objects.create(title='hello', author=self.user, slug='this_is_a_test', body='This is a blog', posted=datetime.now)
        response = self.client.get('/blog/blog_index/')
        self.assertIn(b'This is a blog', response.content)
