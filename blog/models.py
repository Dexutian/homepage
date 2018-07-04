# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from ckeditor.fields import RichTextField

# Create your models here.
class Blog(models.Model):
    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'

    title = models.CharField(max_length=30, unique=True, verbose_name='标题', help_text='博客的标题')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    # body = models.TextField(verbose_name='正文')
    body = RichTextField()
    posted = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return '%s' % (self.title)

    @permalink
    def get_absolute_url(self):
        return 'blog_view', None, {'slug': self.slug}