app_name='blog'
from django.urls import path, re_path
from blog import views

urlpatterns = [
    path('index/', views.blog_list, name='blog_index'),
    re_path('(?P<slug>[^\.]+).html', views.blog_detail, name='blog_view'),
]