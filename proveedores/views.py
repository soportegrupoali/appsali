from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import json
import os
from django.conf import settings

from .models import Proveedor

@login_required(login_url='/')
def proveedor_list(request):
    """Vista para mostrar el listado de proveedores"""
    
    # Filtrado de proveedores
    search_query = request.GET.get('search', '')
    
    proveedores = Proveedor.objects.all()
    
    # Aplicar búsqueda si existe
    if search_query:
        proveedores = proveedores.filter(
            Q(razon_social__icontains=search_query) | 
            Q(nombre_comercial__icontains=search_query) | 
            Q(rfc__icontains=search_query) |
            Q(codigo_erp__icontains=search_query)
        )
    
    proveedores = proveedores.order_by('razon_social')
    
    context = {
        'proveedores': proveedores,
        'search_query': search_query,
        'proveedor_count': proveedores.count(),
    }
    
    return render(request, 'proveedores/list.html', context)

@login_required(login_url='/')
def proveedor_detail(request, proveedor_id):
    """Vista para mostrar el detalle de un proveedor"""
    
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    context = {
        'proveedor': proveedor,
    }
    
    return render(request, 'proveedores/detail.html', context)

@login_required(login_url='/')
def proveedor_create(request):
    """Vista para crear un nuevo proveedor"""
    
    if request.method == 'POST':
        # Obtener datos del formulario
        razon_social = request.POST.get('razon_social', '')
        nombre_comercial = request.POST.get('nombre_comercial', '')
        rfc = request.POST.get('rfc', '')
        codigo_erp = request.POST.get('codigo_erp', '')
        
        # Validaciones básicas
        if not razon_social or not rfc:
            messages.error(request, 'Por favor complete todos los campos obligatorios.')
            return render(request, 'proveedores/create.html')
        
        # Validar que no exista otro proveedor con el mismo RFC
        if Proveedor.objects.filter(rfc=rfc).exists():
            messages.error(request, f'Ya existe un proveedor con el RFC: {rfc}')
            return render(request, 'proveedores/create.html')
        
        # Validar código ERP solo si se proporciona
        if codigo_erp and Proveedor.objects.filter(codigo_erp=codigo_erp).exists():
            messages.error(request, f'Ya existe un proveedor con el código ERP: {codigo_erp}')
            return render(request, 'proveedores/create.html')
        
        try:
            # Crear el proveedor
            proveedor = Proveedor.objects.create(
                razon_social=razon_social,
                nombre_comercial=nombre_comercial if nombre_comercial else razon_social,
                rfc=rfc,
                codigo_erp=codigo_erp if codigo_erp else None
            )
            
            messages.success(request, f'Proveedor "{proveedor.razon_social}" creado exitosamente.')
            return redirect('proveedores:detail', proveedor_id=proveedor.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear proveedor: {str(e)}')
            return render(request, 'proveedores/create.html')
    
    # Si es GET, mostrar el formulario
    return render(request, 'proveedores/create.html')

@login_required(login_url='/')
def proveedor_edit(request, proveedor_id):
    """Vista para editar un proveedor existente"""
    
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        razon_social = request.POST.get('razon_social', '')
        nombre_comercial = request.POST.get('nombre_comercial', '')
        rfc = request.POST.get('rfc', '')
        codigo_erp = request.POST.get('codigo_erp', '')
        
        # Validaciones básicas
        if not razon_social or not rfc:
            messages.error(request, 'Por favor complete todos los campos obligatorios.')
            return render(request, 'proveedores/edit.html', {'proveedor': proveedor})
        
        # Validar que no exista otro proveedor con el mismo RFC (excluyendo el actual)
        if Proveedor.objects.filter(rfc=rfc).exclude(id=proveedor_id).exists():
            messages.error(request, f'Ya existe otro proveedor con el RFC: {rfc}')
            return render(request, 'proveedores/edit.html', {'proveedor': proveedor})
        
        # Validar código ERP solo si se proporciona (excluyendo el actual)
        if codigo_erp and Proveedor.objects.filter(codigo_erp=codigo_erp).exclude(id=proveedor_id).exists():
            messages.error(request, f'Ya existe otro proveedor con el código ERP: {codigo_erp}')
            return render(request, 'proveedores/edit.html', {'proveedor': proveedor})
        
        try:
            # Actualizar el proveedor
            proveedor.razon_social = razon_social
            proveedor.nombre_comercial = nombre_comercial if nombre_comercial else razon_social
            proveedor.rfc = rfc
            proveedor.codigo_erp = codigo_erp if codigo_erp else None
            proveedor.save()
            
            messages.success(request, f'Proveedor "{proveedor.razon_social}" actualizado exitosamente.')
            return redirect('proveedores:detail', proveedor_id=proveedor.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar proveedor: {str(e)}')
            return render(request, 'proveedores/edit.html', {'proveedor': proveedor})
    
    # Si es GET, mostrar el formulario con los datos actuales
    return render(request, 'proveedores/edit.html', {'proveedor': proveedor})

@login_required(login_url='/')
def proveedor_delete(request, proveedor_id):
    """Vista para eliminar un proveedor"""
    
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':
        nombre = proveedor.razon_social
        try:
            proveedor.delete()
            messages.success(request, f'Proveedor "{nombre}" eliminado exitosamente.')
            return redirect('proveedores:list')
        except Exception as e:
            messages.error(request, f'Error al eliminar proveedor: {str(e)}')
    
    return render(request, 'proveedores/delete.html', {'proveedor': proveedor})

@login_required(login_url='/')
def importar_proveedores_json(request):
    """Vista para importar proveedores desde el archivo JSON"""
    
    if request.method == 'POST':
        try:
            # Ruta al archivo JSON
            json_path = os.path.join(settings.STATIC_ROOT, 'datacontpaqi', 'ALI_Proveedores.json')
            if not os.path.exists(json_path):
                json_path = os.path.join(settings.BASE_DIR, 'static', 'datacontpaqi', 'ALI_Proveedores.json')
            
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
                
                if proveedores_creados > 0:
                    messages.success(request, f'Se importaron {proveedores_creados} proveedores exitosamente.')
                else:
                    messages.info(request, 'No se importaron nuevos proveedores.')
                
                if proveedores_existentes > 0:
                    messages.warning(request, f'{proveedores_existentes} proveedores ya existían en la base de datos.')
            else:
                messages.error(request, 'El formato del archivo JSON no es válido.')
        
        except Exception as e:
            messages.error(request, f'Error al importar proveedores: {str(e)}')
        
        return redirect('proveedores:list')
    
    # Si es GET, mostrar la página de confirmación
    return render(request, 'proveedores/import.html')
