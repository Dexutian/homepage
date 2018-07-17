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
    re_path('name_data/(?P<stockcode>[0-9]{1,6})/', views.name_data_by_code, name='name_data_by_code'),
    #每日股票数据
    path('pricedaily_data/',views.pricedaily_data, name='pricedaily_data'),
    path('download_pricedaily_csv/', views.download_pricedaily_csv, name='download_pricedaily_csv'),
    path('progress/', views.progress, name='progress'),
]