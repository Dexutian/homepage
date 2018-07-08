app_name='blog'
from django.urls import path, re_path
from blog import views

urlpatterns = [
    path('index/', views.index, name='blog_index'),
    path('get_category_data/', views.get_category_data, name='get_category_data'),
    re_path('list/(?P<slug>[^\.]+)/', views.list_category, name ='list_category'),
    path('list/', views.blog_list, name='blog_list'),
    re_path('(?P<slug>[^\.]+).html', views.blog_detail, name='blog_view'),
]