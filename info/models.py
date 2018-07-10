from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField('菜单名', max_length=30, unique=True)
    href = models.CharField('链接地址', max_length=30, default="#")
    slug = models.SlugField('slug', max_length=40)
    parent_menu = models.ForeignKey('self', verbose_name='父级菜单', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = "菜单设置"
        verbose_name_plural = "菜单设置"

    def __str__(self):
        return self.name
