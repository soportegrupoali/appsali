# Módulo de Proveedores - SOTALI

## Descripción

El módulo de Proveedores permite gestionar los proveedores del grupo ALI, incluyendo la importación de datos desde archivos JSON generados por CONTPAQ i® y el mantenimiento de información de proveedores.

## Funcionalidades

### ✅ CRUD Completo
- **Crear**: Agregar nuevos proveedores al sistema
- **Leer**: Ver listado y detalles de proveedores
- **Actualizar**: Editar información de proveedores existentes
- **Eliminar**: Remover proveedores del sistema

### ✅ Importación desde JSON
- Importación automática desde archivo `ALI_Proveedores.json`
- Validación de duplicados por RFC y código ERP
- Manejo de valores nulos en código ERP
- Comando de gestión para importación manual

### ✅ Búsqueda y Filtrado
- Búsqueda por razón social, nombre comercial, RFC o código ERP
- Ordenamiento por razón social
- Contador de proveedores

### ✅ Validaciones
- Campos obligatorios (Razón Social, RFC)
- Validación de RFC único
- Validación de código ERP único (cuando se proporciona)
- Conversión automática de RFC y código ERP a mayúsculas

## Estructura del Modelo

```python
class Proveedor(models.Model):
    razon_social = models.CharField(max_length=255)
    nombre_comercial = models.CharField(max_length=255)
    rfc = models.CharField(max_length=20, unique=True)
    codigo_erp = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## URLs Disponibles

- `/proveedores/` - Lista de proveedores
- `/proveedores/create/` - Crear nuevo proveedor
- `/proveedores/<id>/` - Detalle de proveedor
- `/proveedores/<id>/edit/` - Editar proveedor
- `/proveedores/<id>/delete/` - Eliminar proveedor
- `/proveedores/import/` - Importar desde JSON

## Comandos de Gestión

### Importar Proveedores
```bash
python manage.py import_proveedores
```

Este comando:
- Lee el archivo `static/datacontpaqi/ALI_Proveedores.json`
- Valida la estructura del JSON
- Importa proveedores que no existan (por RFC o código ERP)
- Maneja valores nulos en código ERP
- Muestra estadísticas de importación

## Formato del Archivo JSON

El archivo debe tener la siguiente estructura:

```json
{
    "error": false,
    "proveedores": [
        {
            "id": 1,
            "razon_social": "NOMBRE DEL PROVEEDOR S.A. DE C.V.",
            "nombre_comercial": "NOMBRE COMERCIAL",
            "rfc": "RFC123456XXX",
            "codigo_erp": "RFC123456XXX"
        },
        {
            "id": 2,
            "razon_social": "OTRO PROVEEDOR",
            "nombre_comercial": "OTRO PROVEEDOR",
            "rfc": "RFC789012XXX",
            "codigo_erp": null
        }
    ]
}
```

**Nota**: El campo `codigo_erp` puede ser `null` en el JSON y se manejará correctamente.

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
       'proveedores',
       # ...
   ]
   ```

2. **Ejecuta las migraciones**:
   ```bash
   python manage.py makemigrations proveedores
   python manage.py migrate
   ```

3. **Incluye las URLs en el archivo principal**:
   ```python
   urlpatterns = [
       # ...
       path('proveedores/', include('proveedores.urls')),
       # ...
   ]
   ```

## Uso

### Acceso al Módulo
1. Inicia sesión como superusuario
2. Ve al menú principal
3. Haz clic en "Gestionar Proveedores" o usa el enlace en el navbar

### Crear un Proveedor
1. Ve a la lista de proveedores
2. Haz clic en "Nuevo Proveedor"
3. Completa los campos obligatorios (Razón Social y RFC)
4. El código ERP es opcional
5. Guarda el proveedor

### Importar Proveedores
1. Ve a la lista de proveedores
2. Haz clic en "Importar desde JSON"
3. Confirma la importación
4. Revisa los resultados

### Editar/Eliminar
- Usa los botones de acción en la lista de proveedores
- Confirma las acciones de eliminación

## Diferencias con el Módulo de Empresas

### Campo Código ERP
- En proveedores, el código ERP es opcional (puede ser null)
- En empresas, el ID ERP es obligatorio

### Validaciones
- Proveedores: RFC obligatorio, código ERP opcional
- Empresas: RFC e ID ERP obligatorios

### Estructura JSON
- Proveedores: campo `codigo_erp` puede ser null
- Empresas: campo `erp_id` siempre tiene valor

## Mantenimiento

### Archivos Importantes
- `models.py` - Definición del modelo
- `views.py` - Lógica de negocio
- `urls.py` - Configuración de rutas
- `admin.py` - Configuración del admin
- `management/commands/import_proveedores.py` - Comando de importación

### Plantillas
- `list.html` - Lista de proveedores
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
   - Verifica que el código ERP no esté duplicado (si se proporciona)
   - Completa todos los campos obligatorios

3. **Problemas de acceso**:
   - Verifica que el usuario sea superusuario
   - Confirma que la autenticación esté activa

### Logs y Debugging
- Revisa la consola del navegador para errores JavaScript
- Verifica los logs de Django para errores del servidor
- Usa `python manage.py shell` para pruebas interactivas

## Estadísticas de Importación

- **Total de proveedores en JSON**: 528
- **Proveedores importados**: 141
- **Proveedores existentes**: 387
- **Proveedores con código ERP null**: 25

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