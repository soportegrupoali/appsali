from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from django.contrib import messages
from empresas.models import Empresa
from proveedores.models import Proveedor

# Create your views here.
@login_required(login_url='/')
def dashboard(request):
    # Cargar empresas y proveedores para los dropdowns
    empresas = Empresa.objects.all().order_by('nombre_comercial')
    proveedores = Proveedor.objects.all().order_by('nombre_comercial')

    # Datos de ejemplo para el dashboard
    stats = {
        'completed_orders': 12,
        'pending_orders': 5,
        'approved_payments': 8,
        'pending_payments': 3
    }
    
    # Procesar el formulario de nuevo proyecto
    if request.method == 'POST':
        name = request.POST.get('project_name')
        description = request.POST.get('project_description')
        empresa_id = request.POST.get('empresa')
        proveedor_id = request.POST.get('proveedor')
        cost = request.POST.get('project_cost')
        
        print(f"DEBUG: Creating project with data:")
        print(f"  name: {name}")
        print(f"  description: {description}")
        print(f"  empresa_id: {empresa_id}")
        print(f"  proveedor_id: {proveedor_id}")
        print(f"  cost: {cost}")
        
        # Guardar el proyecto en la base de datos
        project = Project.objects.create(
            name=name,
            description=description,
            empresa_id=empresa_id,
            proveedor_id=proveedor_id,
            cost=cost
        )
        
        # Guardar los datos del proyecto en la sesión para usar en workorder
        project_data = {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'empresa': project.empresa.nombre_comercial,
            'proveedor': project.proveedor.nombre_comercial,
            'cost': str(project.cost)
        }
        
        request.session['project_data'] = project_data
        print(f"DEBUG: Session data saved: {project_data}")
        
        messages.success(request, "Proyecto creado correctamente. Continúe con la orden de trabajo.")
        return redirect('workorder:create')
    
    # Enviar los datos al template
    return render(request, 'dashboard.html', {
        'stats': stats,
        'empresas': empresas,
        'proveedores': proveedores,
    })

# Create your views here.
@login_required(login_url='/')
def workorder(request):
    return render(request, 'c_workorder.html')

@login_required(login_url='/')
def workorder_list(request):
    # Esta función mostrará el listado de órdenes de trabajo
    return render(request, 'c_workorder.html')  # Por ahora usamos la misma plantilla

@login_required(login_url='/')
def workorder_create(request):
    # Obtener datos del proyecto de la sesión si existen
    project_data = request.session.get('project_data', None)
    
    # Debug: imprimir los datos para verificar
    print("--- WORKORDER CREATE VIEW ---")
    print(f"DEBUG: Session keys: {list(request.session.keys())}")
    print(f"DEBUG: 'project_data' in session: {'project_data' in request.session}")
    print(f"DEBUG: project_data from session: {project_data}")
    
    context = {
        'project_data': project_data,
    }
    
    print(f"DEBUG: Context being passed to template: {context}")
    
    # Esta función mostrará el formulario para crear una nueva orden de trabajo
    response = render(request, 'workorder.html', context)
    
    # NO borraremos la sesión por ahora para poder depurar
    # if 'project_data' in request.session:
    #     del request.session['project_data']
    #     print("DEBUG: Session data NOT deleted for debugging.")
    
    return response