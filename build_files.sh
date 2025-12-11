#!/bin/bash
set -e

echo "=================================================="
echo "Instalando dependencias"
echo "=================================================="

pip install -r requirements.txt

echo ""
echo "=================================================="
echo "Configurando Django"
echo "=================================================="

export DJANGO_SETTINGS_MODULE=asistencia.settings

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Ejecutando collectstatic..."
python manage.py collectstatic --noinput --clear

echo "Creando superusuario..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistencia.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser creado: admin/admin123')
else:
    print('Superuser ya existe')
"

echo ""
echo "=================================================="
echo "Build completado!"
echo "=================================================="