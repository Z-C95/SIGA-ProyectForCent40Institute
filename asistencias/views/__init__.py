# asistencias/views/__init__.py
from .general_views import home
from .admin_views import (
    admin_dashboard, usuarios_lista, usuarios_crear, usuarios_editar,
    crear_carrera, crear_materia, lista_justificativos,
    aprobar_justificativo, rechazar_justificativo,
    reportes_curso, admin_cursadas, asignar_docente, inscribir_alumnos,
)
from .docente_views import cursos_docente, marcar_asistencia
from .alumno_views import consulta_asistencia, subir_certificado

__all__ = [
    "home",
    "admin_dashboard","usuarios_lista","usuarios_crear","usuarios_editar",
    "crear_carrera","crear_materia","lista_justificativos",
    "aprobar_justificativo","rechazar_justificativo","reportes_curso",
    "admin_cursadas","asignar_docente","inscribir_alumnos",
    "cursos_docente","marcar_asistencia",
    "consulta_asistencia","subir_certificado",
]
