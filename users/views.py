from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Department, JobPosition, UserProfile

# Perfiles de usuario (puedes ampliarlos según necesites)
USER_PROFILES = [
    ('admin', 'Administrador'),
    ('supervisor', 'Supervisor'),
    ('operator', 'Operador'),
    ('guest', 'Invitado')
]

def login(request):
    if request.user.is_authenticated:
        return redirect('menu:index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next', 'menu:index')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('/')

# --- Gestión de Usuarios ---

# --- Configuración inicial para pruebas ---
def setup_initial_departments_and_positions():
    """Función para crear departamentos y puestos iniciales para pruebas"""
    # Verificar si ya existen departamentos
    if Department.objects.count() == 0:
        # Crear departamentos de ejemplo
        admin_dept = Department.objects.create(name="Gerencia de Administración", 
                                      description="Departamento encargado de la administración general")
        operations_dept = Department.objects.create(name="Operaciones", 
                                         description="Departamento de operaciones y logística")
        finance_dept = Department.objects.create(name="Finanzas", 
                                       description="Departamento encargado de la gestión financiera")
        it_dept = Department.objects.create(name="Tecnología", 
                                  description="Departamento de tecnología y sistemas")
        
        # Crear puestos para cada departamento
        JobPosition.objects.create(name="Gerente", department=admin_dept, 
                                 description="Gerente de administración")
        JobPosition.objects.create(name="Asistente Administrativo", department=admin_dept, 
                                 description="Asistente administrativo")
        
        JobPosition.objects.create(name="Jefe de Operaciones", department=operations_dept, 
                                 description="Jefe del departamento de operaciones")
        JobPosition.objects.create(name="Operador", department=operations_dept, 
                                 description="Operador de equipos")
        
        JobPosition.objects.create(name="Director Financiero", department=finance_dept, 
                                 description="Director del área financiera")
        JobPosition.objects.create(name="Contador", department=finance_dept, 
                                 description="Contador general")
        
        JobPosition.objects.create(name="Administrador de Sistemas", department=it_dept, 
                                 description="Administrador de sistemas y redes")
        JobPosition.objects.create(name="Desarrollador", department=it_dept, 
                                 description="Desarrollador de software")
        
        return True
    return False

def ensure_user_profile(user):
    """Ensure the user has a profile, create one if it doesn't exist."""
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(user=user)
    return user.profile

@login_required(login_url='/')
def user_list(request):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para ver la lista de usuarios.')
        return redirect('menu:index')
    
    # Crear departamentos y puestos iniciales si es necesario
    if setup_initial_departments_and_positions():
        messages.success(request, 'Se han creado departamentos y puestos iniciales para pruebas.')
        
        # Asignar el puesto de Gerente al usuario actual
        try:
            admin_dept = Department.objects.get(name="Gerencia de Administración")
            gerente_position = JobPosition.objects.get(name="Gerente", department=admin_dept)
            
            # Asignar puesto al usuario actual
            user_profile = ensure_user_profile(request.user)
            user_profile.job_position = gerente_position
            user_profile.save()
            
            messages.success(request, f'Se ha asignado el puesto de Gerente de Administración a {request.user.username}.')
        except (Department.DoesNotExist, JobPosition.DoesNotExist):
            pass
    
    # Filtrado de usuarios
    search_query = request.GET.get('search', '')
    profile_filter = request.GET.get('profile', '')
    department_filter = request.GET.get('department', '')
    
    users = User.objects.all().prefetch_related('profile__job_position__department')
    
    # Aplicar búsqueda si existe
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profile__job_position__name__icontains=search_query) |
            Q(profile__job_position__department__name__icontains=search_query)
        )
    
    # Filtrar por perfil si se especifica
    if profile_filter == 'admin':
        users = users.filter(is_superuser=True)
    elif profile_filter == 'staff':
        users = users.filter(is_staff=True, is_superuser=False)
    elif profile_filter == 'regular':
        users = users.filter(is_staff=False, is_superuser=False)
    
    # Filtrar por departamento
    if department_filter:
        users = users.filter(profile__job_position__department_id=department_filter)
    
    users = users.order_by('-is_superuser', '-is_staff', 'username')
    
    # Asegurar que todos los usuarios tengan un perfil
    for user in users:
        ensure_user_profile(user)
    
    # Obtener departamentos para el filtro
    departments = Department.objects.all()
    
    context = {
        'users': users,
        'search_query': search_query,
        'profile_filter': profile_filter,
        'department_filter': department_filter,
        'departments': departments,
        'user_count': users.count(),
        'profiles': USER_PROFILES,
    }
    
    return render(request, 'users/list.html', context)

@login_required(login_url='/')
def user_create(request):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear usuarios.')
        return redirect('menu:index')
        
    # Obtener departamentos y puestos de trabajo
    departments = Department.objects.all().order_by('name')
    job_positions = JobPosition.objects.all().order_by('department__name', 'name')
    
    if request.method == 'GET':
        return render(request, 'users/create.html', {
            'profiles': USER_PROFILES,
            'departments': departments,
            'job_positions': job_positions
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crear el usuario (sin activar login automático)
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST.get('email', ''),
                    first_name=request.POST.get('first_name', ''),
                    last_name=request.POST.get('last_name', '')
                )
                
                # Establecer perfil y permisos
                profile = request.POST.get('profile', '')
                is_active = request.POST.get('is_active') == 'on'
                
                # Configurar permisos según el perfil seleccionado
                if profile == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
                elif profile == 'supervisor':
                    user.is_staff = True
                    user.is_superuser = False
                
                user.is_active = is_active
                user.save()
                
                # Crear o actualizar el perfil de usuario con la información del puesto
                user_profile = ensure_user_profile(user)
                
                # Asignar puesto de trabajo si se ha seleccionado
                job_position_id = request.POST.get('job_position')
                if job_position_id:
                    try:
                        job_position = JobPosition.objects.get(id=job_position_id)
                        user_profile.job_position = job_position
                        user_profile.save()
                    except JobPosition.DoesNotExist:
                        pass
                
                # Guardar el perfil en los grupos (puedes expandir esto para más permisos)
                if profile:
                    group, created = Group.objects.get_or_create(name=profile)
                    user.groups.add(group)
                
                messages.success(request, f'Usuario {user.username} creado exitosamente con el perfil de {dict(USER_PROFILES).get(profile, "Usuario")}.')
                return redirect('users:list')
            except Exception as e:
                return render(request, 'users/create.html', {
                    "error": f'Error al crear usuario: {str(e)}',
                    "profiles": USER_PROFILES,
                    'departments': departments,
                    'job_positions': job_positions
                })
        else:
            return render(request, 'users/create.html', {
                "error": 'Las contraseñas no coinciden',
                "profiles": USER_PROFILES,
                'departments': departments,
                'job_positions': job_positions
            })

@login_required(login_url='/')
def user_detail(request, user_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para ver detalles de usuarios.')
        return redirect('menu:index')
    
    user_obj = get_object_or_404(User, id=user_id)
    
    # Asegurar que el usuario tiene un perfil
    user_profile = ensure_user_profile(user_obj)
    
    # Determinar el perfil del usuario
    profile = 'guest'  # Perfil por defecto
    if user_obj.is_superuser:
        profile = 'admin'
    elif user_obj.is_staff:
        profile = 'supervisor'
    elif user_obj.groups.filter(name='operator').exists():
        profile = 'operator'
    
    context = {
        'user_obj': user_obj,
        'user_profile': user_profile,
        'profile': profile,
        'profiles': USER_PROFILES
    }
    
    return render(request, 'users/detail.html', context)

@login_required(login_url='/')
def user_edit(request, user_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para editar usuarios.')
        return redirect('menu:index')
    
    user_obj = get_object_or_404(User, id=user_id)
    
    # Obtener departamentos y puestos de trabajo
    departments = Department.objects.all().order_by('name')
    job_positions = JobPosition.objects.all().order_by('department__name', 'name')
    
    # Asegurar que el usuario tiene un perfil
    user_profile = ensure_user_profile(user_obj)
    
    # Determinar el perfil del usuario
    current_profile = 'guest'  # Perfil por defecto
    if user_obj.is_superuser:
        current_profile = 'admin'
    elif user_obj.is_staff:
        current_profile = 'supervisor'
    elif user_obj.groups.filter(name='operator').exists():
        current_profile = 'operator'
    
    if request.method == 'GET':
        context = {
            'user_obj': user_obj,
            'user_profile': user_profile,
            'current_profile': current_profile,
            'profiles': USER_PROFILES,
            'departments': departments,
            'job_positions': job_positions,
            'current_job_position': user_profile.job_position.id if user_profile.job_position else None,
            'current_department': user_profile.job_position.department.id if user_profile.job_position else None
        }
        return render(request, 'users/edit.html', context)
    
    else:  # POST
        try:
            # Actualizar datos de usuario
            user_obj.first_name = request.POST.get('first_name', '')
            user_obj.last_name = request.POST.get('last_name', '')
            user_obj.email = request.POST.get('email', '')
            user_obj.is_active = request.POST.get('is_active') == 'on'
            
            # Cambiar contraseña solo si se proporciona
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 and password2:
                if password1 == password2:
                    user_obj.set_password(password1)
                else:
                    raise ValueError('Las contraseñas no coinciden')
            
            # Actualizar perfil
            new_profile = request.POST.get('profile', '')
            
            # Eliminar perfiles antiguos
            user_obj.is_staff = False
            user_obj.is_superuser = False
            user_obj.groups.clear()
            
            # Asignar nuevo perfil
            if new_profile == 'admin':
                user_obj.is_staff = True
                user_obj.is_superuser = True
            elif new_profile == 'supervisor':
                user_obj.is_staff = True
            
            # Guardar el perfil en los grupos
            if new_profile:
                group, created = Group.objects.get_or_create(name=new_profile)
                user_obj.groups.add(group)
            
            user_obj.save()
            
            # Actualizar puesto de trabajo
            job_position_id = request.POST.get('job_position')
            if job_position_id:
                try:
                    job_position = JobPosition.objects.get(id=job_position_id)
                    user_profile.job_position = job_position
                    user_profile.save()
                except JobPosition.DoesNotExist:
                    pass
            
            messages.success(request, f'Usuario {user_obj.username} actualizado exitosamente.')
            return redirect('users:detail', user_id=user_obj.id)
            
        except Exception as e:
            context = {
                'user_obj': user_obj,
                'user_profile': user_profile,
                'current_profile': current_profile,
                'profiles': USER_PROFILES,
                'departments': departments,
                'job_positions': job_positions,
                'current_job_position': user_profile.job_position.id if user_profile.job_position else None,
                'current_department': user_profile.job_position.department.id if user_profile.job_position else None,
                'error': f'Error al actualizar usuario: {str(e)}'
            }
            return render(request, 'users/edit.html', context)

@login_required(login_url='/')
def user_delete(request, user_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar usuarios.')
        return redirect('menu:index')
    
    user_obj = get_object_or_404(User, id=user_id)
    
    # No permitir eliminar el propio usuario
    if user_obj == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('users:list')
    
    if request.method == 'POST':
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente.')
        return redirect('users:list')
    
    return render(request, 'users/delete.html', {'user_obj': user_obj})

# --- Gestión de Departamentos ---

@login_required(login_url='/')
def department_list(request):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para gestionar departamentos.')
        return redirect('menu:index')
    
    # Crear departamentos iniciales si es necesario
    setup_initial_departments_and_positions()
    
    departments = Department.objects.all().order_by('name')
    
    return render(request, 'users/departments/list.html', {
        'departments': departments
    })

@login_required(login_url='/')
def department_create(request):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear departamentos.')
        return redirect('menu:index')
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        
        if name:
            try:
                department = Department.objects.create(name=name, description=description)
                messages.success(request, f'Departamento "{department.name}" creado exitosamente.')
                return redirect('users:department_list')
            except Exception as e:
                messages.error(request, f'Error al crear departamento: {str(e)}')
        else:
            messages.error(request, 'El nombre del departamento es obligatorio.')
    
    return render(request, 'users/departments/create.html')

@login_required(login_url='/')
def department_detail(request, dept_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para ver detalles de departamentos.')
        return redirect('menu:index')
    
    department = get_object_or_404(Department, id=dept_id)
    positions = department.positions.all().order_by('name')
    
    return render(request, 'users/departments/detail.html', {
        'department': department,
        'positions': positions
    })

@login_required(login_url='/')
def department_edit(request, dept_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para editar departamentos.')
        return redirect('menu:index')
    
    department = get_object_or_404(Department, id=dept_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        
        if name:
            try:
                department.name = name
                department.description = description
                department.save()
                messages.success(request, f'Departamento "{department.name}" actualizado exitosamente.')
                return redirect('users:department_detail', dept_id=department.id)
            except Exception as e:
                messages.error(request, f'Error al actualizar departamento: {str(e)}')
        else:
            messages.error(request, 'El nombre del departamento es obligatorio.')
    
    return render(request, 'users/departments/edit.html', {
        'department': department
    })

@login_required(login_url='/')
def department_delete(request, dept_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar departamentos.')
        return redirect('menu:index')
    
    department = get_object_or_404(Department, id=dept_id)
    
    # Verificar si hay puestos asociados
    if department.positions.exists():
        messages.error(request, f'No se puede eliminar el departamento "{department.name}" porque tiene puestos de trabajo asociados.')
        return redirect('users:department_detail', dept_id=department.id)
    
    if request.method == 'POST':
        name = department.name
        department.delete()
        messages.success(request, f'Departamento "{name}" eliminado exitosamente.')
        return redirect('users:department_list')
    
    return render(request, 'users/departments/delete.html', {
        'department': department
    })

# --- Gestión de Puestos de Trabajo ---

@login_required(login_url='/')
def job_position_list(request):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para gestionar puestos de trabajo.')
        return redirect('menu:index')
    
    # Crear departamentos iniciales si es necesario
    setup_initial_departments_and_positions()
    
    positions = JobPosition.objects.all().select_related('department').order_by('department__name', 'name')
    
    return render(request, 'users/job_positions/list.html', {
        'positions': positions
    })

@login_required(login_url='/')
def job_position_create(request):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear puestos de trabajo.')
        return redirect('menu:index')
    
    departments = Department.objects.all().order_by('name')
    
    if not departments.exists():
        messages.error(request, 'Debe crear al menos un departamento antes de crear puestos de trabajo.')
        return redirect('users:department_create')
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        department_id = request.POST.get('department', '')
        
        if name and department_id:
            try:
                department = Department.objects.get(id=department_id)
                position = JobPosition.objects.create(
                    name=name,
                    description=description,
                    department=department
                )
                messages.success(request, f'Puesto de trabajo "{position.name}" creado exitosamente.')
                return redirect('users:job_position_list')
            except Department.DoesNotExist:
                messages.error(request, 'El departamento seleccionado no existe.')
            except Exception as e:
                messages.error(request, f'Error al crear puesto de trabajo: {str(e)}')
        else:
            messages.error(request, 'El nombre y el departamento son obligatorios.')
    
    return render(request, 'users/job_positions/create.html', {
        'departments': departments
    })

@login_required(login_url='/')
def job_position_detail(request, pos_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para ver detalles de puestos de trabajo.')
        return redirect('menu:index')
    
    position = get_object_or_404(JobPosition, id=pos_id)
    employees = position.employees.all().select_related('user')
    
    return render(request, 'users/job_positions/detail.html', {
        'position': position,
        'employees': employees
    })

@login_required(login_url='/')
def job_position_edit(request, pos_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para editar puestos de trabajo.')
        return redirect('menu:index')
    
    position = get_object_or_404(JobPosition, id=pos_id)
    departments = Department.objects.all().order_by('name')
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        department_id = request.POST.get('department', '')
        
        if name and department_id:
            try:
                department = Department.objects.get(id=department_id)
                position.name = name
                position.description = description
                position.department = department
                position.save()
                messages.success(request, f'Puesto de trabajo "{position.name}" actualizado exitosamente.')
                return redirect('users:job_position_detail', pos_id=position.id)
            except Department.DoesNotExist:
                messages.error(request, 'El departamento seleccionado no existe.')
            except Exception as e:
                messages.error(request, f'Error al actualizar puesto de trabajo: {str(e)}')
        else:
            messages.error(request, 'El nombre y el departamento son obligatorios.')
    
    return render(request, 'users/job_positions/edit.html', {
        'position': position,
        'departments': departments
    })

@login_required(login_url='/')
def job_position_delete(request, pos_id):
    # Solo permitir a superadministradores
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar puestos de trabajo.')
        return redirect('menu:index')
    
    position = get_object_or_404(JobPosition, id=pos_id)
    
    # Verificar si hay empleados asociados
    if position.employees.exists():
        messages.error(request, f'No se puede eliminar el puesto "{position.name}" porque tiene empleados asociados.')
        return redirect('users:job_position_detail', pos_id=position.id)
    
    if request.method == 'POST':
        name = position.name
        position.delete()
        messages.success(request, f'Puesto de trabajo "{name}" eliminado exitosamente.')
        return redirect('users:job_position_list')
    
    return render(request, 'users/job_positions/delete.html', {
        'position': position
    })