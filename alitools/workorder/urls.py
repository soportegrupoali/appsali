from django.urls import path
from . import views

app_name = 'workorder'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.workorder_list, name='list'),
    path('create/', views.workorder_create, name='create'),
]