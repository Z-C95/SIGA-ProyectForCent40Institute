import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistencia.settings')
django.setup()

from django.core.management import call_command

print("Ejecutando collectstatic...")
call_command('collectstatic', '--noinput', '--clear')

print("Ejecutando migraciones...")
call_command('migrate', '--noinput')

print("Creando superusuario...")
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser creado')