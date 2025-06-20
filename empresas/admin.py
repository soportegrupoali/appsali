from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre_comercial', 'rfc', 'erp_id')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('razon_social', 'nombre_comercial', 'rfc')
    ordering = ('razon_social',)
