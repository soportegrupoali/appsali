from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.proveedor_list, name='list'),
    path('create/', views.proveedor_create, name='create'),
    path('<int:proveedor_id>/', views.proveedor_detail, name='detail'),
    path('<int:proveedor_id>/edit/', views.proveedor_edit, name='edit'),
    path('<int:proveedor_id>/delete/', views.proveedor_delete, name='delete'),
    path('import/', views.importar_proveedores_json, name='import'),
] 