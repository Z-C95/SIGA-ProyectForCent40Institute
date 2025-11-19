from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

# Vistas generales
from .views.general_views import home, editar_perfil, cambiar_password

# Vistas de ADMIN (incluye métricas)
from .views.admin_views import (
    admin_dashboard, admin_cursadas, asignar_docente, inscribir_alumnos,
    usuarios_lista, usuarios_crear, usuarios_editar,
    crear_carrera, crear_materia,
    lista_justificativos, aprobar_justificativo, rechazar_justificativo,
    reportes_curso,
    admin_metricas,
    docente_metricas,
    alumno_metricas,
)

# Vistas de DOCENTE
from .views.docente_views import (
    cursos_docente, marcar_asistencia,
)

# Vistas de ALUMNO
from .views.alumno_views import (
    consulta_asistencia, subir_certificado,
)

app_name = "asistencias"

urlpatterns = [
    # Home
    path("", home, name="home"),

    # Perfil (docente / alumno)
    path("perfil/", editar_perfil, name="editar_perfil"),
    path("perfil/password/", cambiar_password, name="cambiar_password"),

    # Administración general
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/cursadas/", admin_cursadas, name="admin_cursadas"),
    path("admin/asignar-docente/", asignar_docente, name="asignar_docente"),
    path("admin/inscribir-alumnos/", inscribir_alumnos, name="inscribir_alumnos"),

    # Usuarios (Admin)
    path("admin/usuarios/", usuarios_lista, name="usuarios_lista"),
    path("admin/usuarios/nuevo/", usuarios_crear, name="usuarios_crear"),
    path("admin/usuarios/editar/<int:user_id>/", usuarios_editar, name="usuarios_editar"),

    # Carreras y Materias (Admin)
    path("admin/carrera/nueva/", crear_carrera, name="crear_carrera"),
    path("admin/materia/nueva/", crear_materia, name="crear_materia"),

    # Justificativos
    path("admin/justificativos/", lista_justificativos, name="lista_justificativos"),
    path("admin/justificativos/aprobar/<int:asistencia_id>/", aprobar_justificativo, name="aprobar_justificativo"),
    path("admin/justificativos/rechazar/<int:asistencia_id>/", rechazar_justificativo, name="rechazar_justificativo"),

    # Reportes
    path("admin/reportes/", reportes_curso, name="reportes_curso"),

    # ⭐ MÉTRICAS (Admin)
    path("admin/metricas/", admin_metricas, name="admin_metricas"),

    # Docente
    path("docente/cursos/", cursos_docente, name="cursos_docente"),
    path("docente/marcar/<int:curso_id>/", marcar_asistencia, name="marcar_asistencia"),

    # ⭐ MÉTRICAS (Docente)
    path("docente/metricas/", docente_metricas, name="docente_metricas"),

    # Alumno
    path("alumno/asistencias/", consulta_asistencia, name="consulta_asistencia"),
    path("alumno/justificativo/subir/", subir_certificado, name="subir_certificado"),

    # ⭐ MÉTRICAS (Alumno)
    path("alumno/metricas/", alumno_metricas, name="alumno_metricas"),

    # ================================
    # Recuperación de contraseña (Password Reset)
    # ================================
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset_form.html",
            email_template_name="auth/password_reset_email.html",
            subject_template_name="auth/password_reset_subject.txt",
            success_url=reverse_lazy("asistencias:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            success_url=reverse_lazy("asistencias:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
