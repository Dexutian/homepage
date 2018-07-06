from django.contrib import admin
from blog.models import Blog, Category

# Register your models here.
admin.site.register(Blog)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
