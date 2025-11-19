# SIGA  — Django 5

## Setup rápido (SQLite demo)
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # crea admin
python manage.py runserver
```


## Rutas clave
- `/app/docente/cursos/` → listar comisiones y marcar asistencia
- `/app/alumno/asistencias/` → resumen/detalle
- `/app/alumno/justificativo/subir/` → subir certificado
- `/app/admin/justificativos/` → validar
- `/app/admin/reportes/` → reportes por comisión
- `/app/usuarios/` → administración simple de usuarios (demo)

> Usuario custom `AUTH_USER_MODEL = 'asistencias.User'` alineado con tabla `users`.
