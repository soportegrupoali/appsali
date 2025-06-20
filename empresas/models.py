from django.db import models

class Empresa(models.Model):
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    nombre_comercial = models.CharField(max_length=255, verbose_name="Nombre Comercial")
    rfc = models.CharField(max_length=20, verbose_name="RFC", unique=True)
    erp_id = models.IntegerField(verbose_name="ID en ERP", unique=True)
    direccion = models.TextField(verbose_name="Dirección")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['razon_social']
    
    def __str__(self):
        return self.nombre_comercial
