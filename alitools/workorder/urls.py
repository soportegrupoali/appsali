from django.urls import path
from . import views

app_name = 'workorder'

urlpatterns = [
    path('workorder/', views.dashboard, name='dashboard'),
    path('workorder/', views.workorder_list, name='list'),
    path('workorder/create/', views.workorder_create, name='create'),
]