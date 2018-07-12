app_name='stock'
from django.urls import path, re_path
from stock import views

urlpatterns = [
    path('index/', views.index, name='stock_index'),
    path('get_menu_data/', views.get_menu_data, name='get_menu_data'),
    #股票名称
    path('name_file/', views.name_file, name='name_file'),
    path('upload_name_file', views.upload_name_file, name='upload_name_file'),
    path('update_name/', views.update_name, name='update_name'),
    path('name_data/', views.name_data, name='name_data'),
]