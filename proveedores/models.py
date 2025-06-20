from django.db import models

# Create your models here.

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    nombre_comercial = models.CharField(max_length=255, verbose_name="Nombre Comercial")
    rfc = models.CharField(max_length=20, verbose_name="RFC", unique=True)
    codigo_erp = models.CharField(max_length=50, verbose_name="Código en ERP", unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['razon_social']
    
    def __str__(self):
        return self.nombre_comercial
