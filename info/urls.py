app_name='info'
from django.urls import path, re_path
from info import views

urlpatterns = [
    path('get_menu_data/', views.get_menu_data, name="get_menu_data"),
]