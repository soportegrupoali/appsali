import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from proveedores.models import Proveedor

class Command(BaseCommand):
    help = 'Importa proveedores desde el archivo JSON'
    
    def handle(self, *args, **options):
        try:
            # Ruta al archivo JSON
            json_path = os.path.join(settings.STATIC_ROOT, 'datacontpaqi', 'ALI_Proveedores.json')
            if not os.path.exists(json_path):
                json_path = os.path.join(settings.BASE_DIR, 'static', 'datacontpaqi', 'ALI_Proveedores.json')
            
            if not os.path.exists(json_path):
                self.stdout.write(self.style.ERROR(f'No se encontró el archivo JSON en {json_path}'))
                return
            
            # Leer el archivo JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'error' in data and not data['error'] and 'proveedores' in data:
                proveedores_creados = 0
                proveedores_existentes = 0
                
                for proveedor_data in data['proveedores']:
                    # Verificar si ya existe un proveedor con el mismo RFC
                    if Proveedor.objects.filter(rfc=proveedor_data['rfc']).exists():
                        proveedores_existentes += 1
                        continue
                    
                    # Verificar código ERP solo si no es null
                    codigo_erp = proveedor_data.get('codigo_erp')
                    if codigo_erp and Proveedor.objects.filter(codigo_erp=codigo_erp).exists():
                        proveedores_existentes += 1
                        continue
                    
                    # Crear el proveedor
                    Proveedor.objects.create(
                        razon_social=proveedor_data['razon_social'],
                        nombre_comercial=proveedor_data['nombre_comercial'],
                        rfc=proveedor_data['rfc'],
                        codigo_erp=codigo_erp
                    )
                    proveedores_creados += 1
                
                self.stdout.write(self.style.SUCCESS(f'Se importaron {proveedores_creados} proveedores exitosamente.'))
                
                if proveedores_existentes > 0:
                    self.stdout.write(self.style.WARNING(f'{proveedores_existentes} proveedores ya existían en la base de datos.'))
            else:
                self.stdout.write(self.style.ERROR('El formato del archivo JSON no es válido.'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al importar proveedores: {str(e)}')) 