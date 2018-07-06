# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Blog(models.Model):
    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'

    title = models.CharField(max_length=30, unique=True, verbose_name='标题', help_text='博客的标题')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    # body = models.TextField(verbose_name='正文')
    body = RichTextUploadingField(verbose_name='正文')
    posted = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return '%s' % (self.title)

    @permalink
    def get_absolute_url(self):
        return 'blog_view', None, {'slug': self.slug}

class Category(models.Model):
    name = models.CharField('分类名', max_length=30, unique=True)
    slug = models.SlugField('slug', max_length=40)
    parent_category = models.ForeignKey('self', verbose_name='父级分类', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"

    def __str__(self):
        return self.name