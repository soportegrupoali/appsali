#!/bin/bash

# Script para levantar el proyecto AppsALI con Docker

echo "🚀 Iniciando AppsALI con Docker..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Detener contenedores existentes si los hay
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

# Construir las imágenes
echo "🔨 Construyendo imágenes..."
docker-compose build

# Levantar los servicios
echo "📦 Levantando servicios..."
docker-compose up -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 10

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
docker-compose exec web python manage.py migrate

# Crear superusuario si no existe
echo "👤 Creando superusuario..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@appsali.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('El superusuario ya existe')
"

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
docker-compose exec web python manage.py collectstatic --noinput

echo "✅ ¡Proyecto AppsALI iniciado correctamente!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - Aplicación Django: http://localhost:8000"
echo "   - pgAdmin: http://localhost:5050"
echo ""
echo "👤 Credenciales:"
echo "   - Django Admin: admin/admin123"
echo "   - pgAdmin: admin@appsali.com/admin123"
echo ""
echo "📋 Comandos útiles:"
echo "   - Ver logs: docker-compose logs -f"
echo "   - Detener: docker-compose down"
echo "   - Reiniciar: docker-compose restart" 