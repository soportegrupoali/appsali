import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from empresas.models import Empresa

class Command(BaseCommand):
    help = 'Importa empresas desde el archivo JSON'
    
    def handle(self, *args, **options):
        try:
            # Ruta al archivo JSON
            json_path = os.path.join(settings.STATIC_ROOT, 'datacontpaqi', 'ALI_Empresas.json')
            if not os.path.exists(json_path):
                json_path = os.path.join(settings.BASE_DIR, 'static', 'datacontpaqi', 'ALI_Empresas.json')
            
            if not os.path.exists(json_path):
                self.stdout.write(self.style.ERROR(f'No se encontró el archivo JSON en {json_path}'))
                return
            
            # Leer el archivo JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'error' in data and not data['error'] and 'cuentas_pagadoras' in data:
                empresas_creadas = 0
                empresas_existentes = 0
                
                for empresa_data in data['cuentas_pagadoras']:
                    # Verificar si ya existe una empresa con el mismo RFC o ERP ID
                    if Empresa.objects.filter(Q(rfc=empresa_data['rfc']) | Q(erp_id=empresa_data['erp_id'])).exists():
                        empresas_existentes += 1
                        continue
                    
                    # Crear la empresa
                    Empresa.objects.create(
                        razon_social=empresa_data['razon_social'],
                        nombre_comercial=empresa_data['nombre_comercial'],
                        rfc=empresa_data['rfc'],
                        erp_id=empresa_data['erp_id'],
                        direccion=empresa_data['direccion']
                    )
                    empresas_creadas += 1
                
                self.stdout.write(self.style.SUCCESS(f'Se importaron {empresas_creadas} empresas exitosamente.'))
                
                if empresas_existentes > 0:
                    self.stdout.write(self.style.WARNING(f'{empresas_existentes} empresas ya existían en la base de datos.'))
            else:
                self.stdout.write(self.style.ERROR('El formato del archivo JSON no es válido.'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al importar empresas: {str(e)}'))