"""homepage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homepage import views
from django.urls import include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

auth_patterns = [
	path('login/', auth_views.login, {'template_name': 'index/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'index/logged_out.html', 'next_page': 'index'}, name='logout'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('auth/', include(auth_patterns)),
    path('blog/', include("blog.urls")),
    path('info/', include("info.urls")),
    path('stock/', include("stock.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
