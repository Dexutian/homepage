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
    re_path('pricedaily_data/(?P<stockcode>[0-9]{1,6})/', views.pricedaily_data_by_code, name='pricedaily_data_by_code'),
    path('download_pricedaily_csv/', views.download_pricedaily_csv, name='download_pricedaily_csv'),
    path('updatecsv2database/', views.updatecsv2database, name='updatecsv2database'),
    path('delete_pricedaily_csv/', views.delete_pricedaily_csv, name='delete_pricedaily_csv'),
    path('progress/', views.progress, name='progress'),
    #大单交易数据
    path('dadang_exchange/', views.dadang_exchange, name='dadang_exchange'),
    re_path('dadang_exchange/(?P<stockcode>[0-9]{1,6})/', views.dadang_exchange_by_code, name='dadang_exchange_by_code'),
    path('update_dadang_exchange/', views.update_dadang_exchange, name='update_dadang_exchange'),
    #数据可视化
    re_path('graphic/(?P<code>[0-9]{6})/', views.graphic, name = 'graphic'),
    path('stock_contrast/', views.stock_contrast, name='stock_contrast'),
    path('get_stock_code/', views.get_stock_code, name='get_stock_code'),
    path('get_contrast_data/', views.get_contrast_data, name='get_contrast_data'),
]