"""
URL configuration for alitools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from users import views as users_views
from menu import views as menu_views
from alitools.workorder import views as workorder_views
from empresas import views as empresas_views
from proveedores import views as proveedores_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users_views.login, name='home_login'),  # Ruta raíz apunta directamente al login
    path('users/', include('users.urls')),
    path('menu/', include('menu.urls')),
    path('workorder/', workorder_views.dashboard, name='workorder_dashboard'),
    path('workorder/create/', workorder_views.workorder_create, name='workorder_create'),
    path('empresas/', include('empresas.urls')),
    path('proveedores/', include('proveedores.urls')),
]
