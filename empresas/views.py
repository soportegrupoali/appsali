from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import json
import os
from django.conf import settings

from .models import Empresa

@login_required(login_url='/')
def empresa_list(request):
    """Vista para mostrar el listado de empresas"""
    
    # Filtrado de empresas
    search_query = request.GET.get('search', '')
    
    empresas = Empresa.objects.all()
    
    # Aplicar búsqueda si existe
    if search_query:
        empresas = empresas.filter(
            Q(razon_social__icontains=search_query) | 
            Q(nombre_comercial__icontains=search_query) | 
            Q(rfc__icontains=search_query)
        )
    
    empresas = empresas.order_by('razon_social')
    
    context = {
        'empresas': empresas,
        'search_query': search_query,
        'empresa_count': empresas.count(),
    }
    
    return render(request, 'empresas/list.html', context)

@login_required(login_url='/')
def empresa_detail(request, empresa_id):
    """Vista para mostrar el detalle de una empresa"""
    
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    context = {
        'empresa': empresa,
    }
    
    return render(request, 'empresas/detail.html', context)

@login_required(login_url='/')
def empresa_create(request):
    """Vista para crear una nueva empresa"""
    
    if request.method == 'POST':
        # Obtener datos del formulario
        razon_social = request.POST.get('razon_social', '')
        nombre_comercial = request.POST.get('nombre_comercial', '')
        rfc = request.POST.get('rfc', '')
        erp_id = request.POST.get('erp_id', '')
        direccion = request.POST.get('direccion', '')
        
        # Validaciones básicas
        if not razon_social or not rfc or not erp_id:
            messages.error(request, 'Por favor complete todos los campos obligatorios.')
            return render(request, 'empresas/create.html')
        
        # Validar que no exista otra empresa con el mismo RFC o ERP ID
        if Empresa.objects.filter(rfc=rfc).exists():
            messages.error(request, f'Ya existe una empresa con el RFC: {rfc}')
            return render(request, 'empresas/create.html')
            
        if Empresa.objects.filter(erp_id=erp_id).exists():
            messages.error(request, f'Ya existe una empresa con el ID ERP: {erp_id}')
            return render(request, 'empresas/create.html')
        
        try:
            # Crear la empresa
            empresa = Empresa.objects.create(
                razon_social=razon_social,
                nombre_comercial=nombre_comercial if nombre_comercial else razon_social,
                rfc=rfc,
                erp_id=erp_id,
                direccion=direccion
            )
            
            messages.success(request, f'Empresa "{empresa.razon_social}" creada exitosamente.')
            return redirect('empresas:detail', empresa_id=empresa.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear empresa: {str(e)}')
            return render(request, 'empresas/create.html')
    
    # Si es GET, mostrar el formulario
    return render(request, 'empresas/create.html')

@login_required(login_url='/')
def empresa_edit(request, empresa_id):
    """Vista para editar una empresa existente"""
    
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        razon_social = request.POST.get('razon_social', '')
        nombre_comercial = request.POST.get('nombre_comercial', '')
        rfc = request.POST.get('rfc', '')
        erp_id = request.POST.get('erp_id', '')
        direccion = request.POST.get('direccion', '')
        
        # Validaciones básicas
        if not razon_social or not rfc or not erp_id:
            messages.error(request, 'Por favor complete todos los campos obligatorios.')
            return render(request, 'empresas/edit.html', {'empresa': empresa})
        
        # Validar que no exista otra empresa con el mismo RFC o ERP ID (excluyendo la actual)
        if Empresa.objects.filter(rfc=rfc).exclude(id=empresa_id).exists():
            messages.error(request, f'Ya existe otra empresa con el RFC: {rfc}')
            return render(request, 'empresas/edit.html', {'empresa': empresa})
            
        if Empresa.objects.filter(erp_id=erp_id).exclude(id=empresa_id).exists():
            messages.error(request, f'Ya existe otra empresa con el ID ERP: {erp_id}')
            return render(request, 'empresas/edit.html', {'empresa': empresa})
        
        try:
            # Actualizar la empresa
            empresa.razon_social = razon_social
            empresa.nombre_comercial = nombre_comercial if nombre_comercial else razon_social
            empresa.rfc = rfc
            empresa.erp_id = erp_id
            empresa.direccion = direccion
            empresa.save()
            
            messages.success(request, f'Empresa "{empresa.razon_social}" actualizada exitosamente.')
            return redirect('empresas:detail', empresa_id=empresa.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar empresa: {str(e)}')
            return render(request, 'empresas/edit.html', {'empresa': empresa})
    
    # Si es GET, mostrar el formulario con los datos actuales
    return render(request, 'empresas/edit.html', {'empresa': empresa})

@login_required(login_url='/')
def empresa_delete(request, empresa_id):
    """Vista para eliminar una empresa"""
    
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        nombre = empresa.razon_social
        try:
            empresa.delete()
            messages.success(request, f'Empresa "{nombre}" eliminada exitosamente.')
            return redirect('empresas:list')
        except Exception as e:
            messages.error(request, f'Error al eliminar empresa: {str(e)}')
    
    return render(request, 'empresas/delete.html', {'empresa': empresa})

@login_required(login_url='/')
def importar_empresas_json(request):
    """Vista para importar empresas desde el archivo JSON"""
    
    if request.method == 'POST':
        try:
            # Ruta al archivo JSON
            json_path = os.path.join(settings.STATIC_ROOT, 'datacontpaqi', 'ALI_Empresas.json')
            if not os.path.exists(json_path):
                json_path = os.path.join(settings.BASE_DIR, 'static', 'datacontpaqi', 'ALI_Empresas.json')
            
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
                
                if empresas_creadas > 0:
                    messages.success(request, f'Se importaron {empresas_creadas} empresas exitosamente.')
                else:
                    messages.info(request, 'No se importaron nuevas empresas.')
                
                if empresas_existentes > 0:
                    messages.warning(request, f'{empresas_existentes} empresas ya existían en la base de datos.')
            else:
                messages.error(request, 'El formato del archivo JSON no es válido.')
        
        except Exception as e:
            messages.error(request, f'Error al importar empresas: {str(e)}')
        
        return redirect('empresas:list')
    
    # Si es GET, mostrar la página de confirmación
    return render(request, 'empresas/import.html')
