# 🐳 AppsALI - Guía de Docker

Esta guía te ayudará a levantar el proyecto AppsALI usando Docker.

## 📋 Prerrequisitos

- Docker Desktop instalado
- Docker Compose instalado
- Al menos 4GB de RAM disponible

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

```bash
# Ejecutar el script de inicio
./start.sh
```

### Opción 2: Comandos Manuales

```bash
# 1. Construir las imágenes
docker-compose build

# 2. Levantar los servicios
docker-compose up -d

# 3. Ejecutar migraciones
docker-compose exec web python manage.py migrate

# 4. Crear superusuario
docker-compose exec web python manage.py createsuperuser

# 5. Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

## 🌐 URLs Disponibles

- **Aplicación Django**: http://localhost:8000
- **pgAdmin**: http://localhost:5050

## 👤 Credenciales por Defecto

### Django Admin
- **Usuario**: admin
- **Contraseña**: admin123

### pgAdmin
- **Email**: admin@appsali.com
- **Contraseña**: admin123

## 📁 Estructura de Servicios

### 🐘 Base de Datos (PostgreSQL)
- **Puerto**: 5432
- **Base de datos**: alitools
- **Usuario**: ali_user
- **Contraseña**: ali_password

### 🌐 Aplicación Web (Django)
- **Puerto**: 8000
- **Framework**: Django 5.2.3
- **Base de datos**: PostgreSQL

### 🗄️ pgAdmin
- **Puerto**: 5050
- **Propósito**: Interfaz web para administrar PostgreSQL

## 🔧 Comandos Útiles

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Ver logs de un servicio específico
```bash
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f pgadmin
```

### Detener todos los servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ CUIDADO: elimina datos)
```bash
docker-compose down -v
```

### Reiniciar un servicio específico
```bash
docker-compose restart web
```

### Ejecutar comandos en el contenedor
```bash
# Shell de Django
docker-compose exec web python manage.py shell

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

## 🗂️ Volúmenes

- **postgres_data**: Datos de PostgreSQL
- **pdf_storage**: Archivos PDF generados
- **pgadmin_data**: Configuración de pgAdmin
- **static_volume**: Archivos estáticos de Django

## 🔍 Solución de Problemas

### Error de conexión a la base de datos
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db
```

### Error de permisos
```bash
# Reconstruir la imagen
docker-compose build --no-cache
```

### Puerto ocupado
```bash
# Verificar qué está usando el puerto
lsof -i :8000
lsof -i :5432
lsof -i :5050
```

### Limpiar todo y empezar de nuevo
```bash
# Detener y eliminar todo
docker-compose down -v
docker system prune -a

# Reconstruir desde cero
./start.sh
```

## 📝 Variables de Entorno

Puedes crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DB_NAME=alitools
DB_USER=ali_user
DB_PASSWORD=ali_password
DB_HOST=db
DB_PORT=5432

# Django
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@appsali.com
PGADMIN_DEFAULT_PASSWORD=admin123
```

## 🛠️ Desarrollo

### Agregar nuevas dependencias
1. Agrega la dependencia a `requirements.txt`
2. Reconstruye la imagen: `docker-compose build`
3. Reinicia el servicio: `docker-compose restart web`

### Cambios en el código
Los cambios en el código se reflejan automáticamente gracias al volumen montado.

### Cambios en la base de datos
```bash
# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate
```

## 📞 Soporte

Si tienes problemas, puedes:

1. Revisar los logs: `docker-compose logs -f`
2. Verificar el estado de los contenedores: `docker-compose ps`
3. Reconstruir todo: `./start.sh`

¡Disfruta desarrollando con AppsALI! 🎉 