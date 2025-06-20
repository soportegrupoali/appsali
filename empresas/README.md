# Módulo de Empresas - SOTALI

## Descripción

El módulo de Empresas permite gestionar las empresas del grupo ALI, incluyendo la importación de datos desde archivos JSON generados por CONTPAQ i® y el mantenimiento de información empresarial.

## Funcionalidades

### ✅ CRUD Completo
- **Crear**: Agregar nuevas empresas al sistema
- **Leer**: Ver listado y detalles de empresas
- **Actualizar**: Editar información de empresas existentes
- **Eliminar**: Remover empresas del sistema

### ✅ Importación desde JSON
- Importación automática desde archivo `ALI_Empresas.json`
- Validación de duplicados por RFC e ID ERP
- Comando de gestión para importación manual

### ✅ Búsqueda y Filtrado
- Búsqueda por razón social, nombre comercial o RFC
- Ordenamiento por razón social
- Contador de empresas

### ✅ Validaciones
- Campos obligatorios (Razón Social, RFC, ID ERP)
- Validación de RFC único
- Validación de ID ERP único
- Conversión automática de RFC a mayúsculas

## Estructura del Modelo

```python
class Empresa(models.Model):
    razon_social = models.CharField(max_length=255)
    nombre_comercial = models.CharField(max_length=255)
    rfc = models.CharField(max_length=20, unique=True)
    erp_id = models.IntegerField(unique=True)
    direccion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## URLs Disponibles

- `/empresas/` - Lista de empresas
- `/empresas/create/` - Crear nueva empresa
- `/empresas/<id>/` - Detalle de empresa
- `/empresas/<id>/edit/` - Editar empresa
- `/empresas/<id>/delete/` - Eliminar empresa
- `/empresas/import/` - Importar desde JSON

## Comandos de Gestión

### Importar Empresas
```bash
python manage.py import_empresas
```

Este comando:
- Lee el archivo `static/datacontpaqi/ALI_Empresas.json`
- Valida la estructura del JSON
- Importa empresas que no existan (por RFC o ID ERP)
- Muestra estadísticas de importación

## Formato del Archivo JSON

El archivo debe tener la siguiente estructura:

```json
{
    "error": false,
    "cuentas_pagadoras": [
        {
            "id": 1,
            "razon_social": "NOMBRE DE LA EMPRESA S.A. DE C.V.",
            "nombre_comercial": "NOMBRE COMERCIAL",
            "rfc": "RFC123456XXX",
            "erp_id": 1,
            "direccion": "Dirección completa de la empresa"
        }
    ]
}
```

## Características Técnicas

### Frontend
- **Framework**: Bootstrap 5.3.2
- **Iconos**: Font Awesome 6.4.0
- **Responsive**: Diseño adaptativo para móviles
- **Validación**: JavaScript en tiempo real
- **Animaciones**: Transiciones suaves

### Backend
- **Framework**: Django 5.2.3
- **Base de datos**: SQLite (configurable)
- **Autenticación**: Sistema de login requerido
- **Permisos**: Acceso restringido a superusuarios

### Seguridad
- Protección CSRF en todos los formularios
- Validación de datos en servidor
- Sanitización de entradas
- Control de acceso por autenticación

## Instalación y Configuración

1. **Asegúrate de que la aplicación esté en `INSTALLED_APPS`**:
   ```python
   INSTALLED_APPS = [
       # ...
       'empresas',
       # ...
   ]
   ```

2. **Ejecuta las migraciones**:
   ```bash
   python manage.py makemigrations empresas
   python manage.py migrate
   ```

3. **Incluye las URLs en el archivo principal**:
   ```python
   urlpatterns = [
       # ...
       path('empresas/', include('empresas.urls')),
       # ...
   ]
   ```

4. **Configura STATIC_ROOT en settings.py**:
   ```python
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```

## Uso

### Acceso al Módulo
1. Inicia sesión como superusuario
2. Ve al menú principal
3. Haz clic en "Gestionar Empresas" o usa el enlace en el navbar

### Crear una Empresa
1. Ve a la lista de empresas
2. Haz clic en "Nueva Empresa"
3. Completa los campos obligatorios
4. Guarda la empresa

### Importar Empresas
1. Ve a la lista de empresas
2. Haz clic en "Importar desde JSON"
3. Confirma la importación
4. Revisa los resultados

### Editar/Eliminar
- Usa los botones de acción en la lista de empresas
- Confirma las acciones de eliminación

## Mantenimiento

### Archivos Importantes
- `models.py` - Definición del modelo
- `views.py` - Lógica de negocio
- `urls.py` - Configuración de rutas
- `admin.py` - Configuración del admin
- `management/commands/import_empresas.py` - Comando de importación

### Plantillas
- `list.html` - Lista de empresas
- `create.html` - Formulario de creación
- `edit.html` - Formulario de edición
- `detail.html` - Vista de detalle
- `delete.html` - Confirmación de eliminación
- `import.html` - Página de importación

## Troubleshooting

### Problemas Comunes

1. **Error al importar JSON**:
   - Verifica que el archivo existe en `static/datacontpaqi/`
   - Valida la estructura del JSON
   - Revisa los permisos del archivo

2. **Error de validación**:
   - Asegúrate de que el RFC sea único
   - Verifica que el ID ERP no esté duplicado
   - Completa todos los campos obligatorios

3. **Problemas de acceso**:
   - Verifica que el usuario sea superusuario
   - Confirma que la autenticación esté activa

### Logs y Debugging
- Revisa la consola del navegador para errores JavaScript
- Verifica los logs de Django para errores del servidor
- Usa `python manage.py shell` para pruebas interactivas

## Contribución

Para contribuir al módulo:
1. Sigue las convenciones de Django
2. Mantén la consistencia en el código
3. Documenta los cambios
4. Prueba las funcionalidades antes de commit

## Versión
- **Versión actual**: 1.0.0
- **Última actualización**: Diciembre 2024
- **Compatibilidad**: Django 5.2+ 