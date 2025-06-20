import json
import os
import django
import sys

# Configurar el entorno de Django
sys.path.append('/Users/dannycen/Desktop/appsali')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alitools.settings')
django.setup()

from django.db.models import Q
from empresas.models import Empresa

def import_empresas():
    try:
        # Ruta al archivo JSON
        json_path = os.path.join('/Users/dannycen/Desktop/appsali/static/datacontpaqi', 'ALI_Empresas.json')
        
        if not os.path.exists(json_path):
            print(f'No se encontró el archivo JSON en {json_path}')
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
                    print(f"Empresa ya existe: {empresa_data['nombre_comercial']}")
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
                print(f"Empresa creada: {empresa_data['nombre_comercial']}")
            
            print(f'Se importaron {empresas_creadas} empresas exitosamente.')
            
            if empresas_existentes > 0:
                print(f'{empresas_existentes} empresas ya existían en la base de datos.')
        else:
            print('El formato del archivo JSON no es válido.')
    
    except Exception as e:
        print(f'Error al importar empresas: {str(e)}')

if __name__ == '__main__':
    import_empresas()