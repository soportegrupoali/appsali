from django.contrib import admin
from .models import Department, JobPosition, UserProfile

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'description', 'created_at')
    search_fields = ('name', 'department__name')
    list_filter = ('department', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_position', 'phone', 'employee_id')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'job_position__name')
    list_filter = ('job_position__department',)
