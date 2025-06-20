from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.empresa_list, name='list'),
    path('<int:empresa_id>/', views.empresa_detail, name='detail'),
    path('create/', views.empresa_create, name='create'),
    path('<int:empresa_id>/edit/', views.empresa_edit, name='edit'),
    path('<int:empresa_id>/delete/', views.empresa_delete, name='delete'),
    path('import/', views.importar_empresas_json, name='import'),
]