from django.db import models
from empresas.models import Empresa
from proveedores.models import Proveedor

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Proyecto")
    description = models.TextField(verbose_name="Descripción")
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, verbose_name="Empresa")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, verbose_name="Proveedor")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del Proyecto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
# Create your models here.
class WorkOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Borrador'),
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
        ('completed', 'Completada'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_orders')
    code = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Datos del contratista
    contractor_name = models.CharField(max_length=200)
    contractor_rfc = models.CharField(max_length=20)
    contractor_address = models.TextField()
    contractor_phone = models.CharField(max_length=20)
    contractor_email = models.EmailField()
    
    # Datos del representante legal
    legal_representative = models.CharField(max_length=200)
    legal_representative_id = models.CharField(max_length=50)
    
    # Descripción del trabajo
    work_description = models.TextField()
    
    # Importes
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Orden de trabajo #{self.code}"
