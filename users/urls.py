from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Gestión de usuarios
    path('management/', views.user_list, name='list'),
    path('management/create/', views.user_create, name='create'),
    path('management/<int:user_id>/', views.user_detail, name='detail'),
    path('management/<int:user_id>/edit/', views.user_edit, name='edit'),
    path('management/<int:user_id>/delete/', views.user_delete, name='delete'),
    
    # Gestión de departamentos
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:dept_id>/', views.department_detail, name='department_detail'),
    path('departments/<int:dept_id>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:dept_id>/delete/', views.department_delete, name='department_delete'),
    
    # Gestión de puestos
    path('job-positions/', views.job_position_list, name='job_position_list'),
    path('job-positions/create/', views.job_position_create, name='job_position_create'),
    path('job-positions/<int:pos_id>/', views.job_position_detail, name='job_position_detail'),
    path('job-positions/<int:pos_id>/edit/', views.job_position_edit, name='job_position_edit'),
    path('job-positions/<int:pos_id>/delete/', views.job_position_delete, name='job_position_delete'),
]