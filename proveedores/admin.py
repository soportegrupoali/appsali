from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre_comercial', 'rfc', 'codigo_erp')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('razon_social', 'nombre_comercial', 'rfc', 'codigo_erp')
    ordering = ('razon_social',)
