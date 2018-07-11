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

class Name(models.Model):
	companycode = models.CharField(max_length = 10)
	companyabb = models.CharField(max_length = 10)
	stockexchangeno= models.CharField(max_length = 10)
	stockstyle = models.CharField(max_length = 10)
	stockcode = models.CharField(max_length = 10)
	stockabb = models.CharField(max_length = 10)
	listingdate = models.DateField(null=True)
	generalcapital = models.FloatField()
	circulatingcapital = models.FloatField()
	bysector = models.CharField(max_length = 10)
	filename = models.CharField(max_length = 10, null=True)
	startdate = models.DateField(null = True)
	enddate = models.DateField(null=True)
	path = models.CharField(max_length = 50, null=True)
	fupdatetime = models.DateField(null=True)

	def __str__(self):
		return self.stockabb

	class Meta:
		permissions = (
			('views_name_manage', '名称管理'),
		)
		verbose_name = "股票名称"
		verbose_name_plural = "股票名称"