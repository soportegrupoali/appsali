from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Departamento")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['name']

class JobPosition(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Puesto")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="positions", verbose_name="Departamento")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    def __str__(self):
        return f"{self.name} - {self.department.name}"
    
    class Meta:
        verbose_name = "Puesto de Trabajo"
        verbose_name_plural = "Puestos de Trabajo"
        ordering = ['department__name', 'name']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Usuario")
    job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees", verbose_name="Puesto de Trabajo")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    employee_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID de Empleado")
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
