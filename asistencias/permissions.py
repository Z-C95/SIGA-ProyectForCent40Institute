# asistencias/permissions.py
from .models import User

def is_admin(u):
    return u.is_authenticated and getattr(u, "rol", None) == User.Rol.ADMIN

def is_docente(u):
    return u.is_authenticated and getattr(u, "rol", None) == User.Rol.DOCENTE

def is_alumno(u):
    return u.is_authenticated and getattr(u, "rol", None) == User.Rol.ALUMNO
