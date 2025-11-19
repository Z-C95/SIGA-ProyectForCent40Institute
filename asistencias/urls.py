# asistencias/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

# Vistas generales
from .views.general_views import home, editar_perfil, cambiar_password

# Vistas de ADMIN
from .views.admin_views import (
    admin_dashboard,
    admin_cursadas,
    cursada_detalle,      # Detalle de cursada
    asignar_docente,
    inscribir_alumnos,

    # Usuarios
    usuarios_lista,
    usuarios_crear,
    usuarios_editar,
    usuarios_eliminar,

    # Carreras / Materias
    carreras_lista,
    carrera_detalle,
    carrera_editar,
    carrera_eliminar,
    crear_carrera,

    materias_lista,
    materia_detalle,
    materia_editar,
    materia_eliminar,
    crear_materia,

    # Justificativos
    lista_justificativos,
    aprobar_justificativo,
    rechazar_justificativo,

    # Reportes
    reportes_curso,

    # Métricas (solo Admin; Docente y Alumno van en sus views)
    admin_metricas,
)

# Vistas de DOCENTE
from .views.docente_views import (
    cursos_docente,
    marcar_asistencia,
    docente_dashboard,
    docente_metricas,
)

# Vistas de ALUMNO
from .views.alumno_views import (
    alumno_dashboard,       # Dashboard del alumno
    consulta_asistencia,
    subir_certificado,
    alumno_metricas,        # Métricas del alumno
)

app_name = "asistencias"

urlpatterns = [
    # =========================
    # Home / Perfil
    # =========================
    path("", home, name="home"),

    path("perfil/", editar_perfil, name="editar_perfil"),
    path("perfil/password/", cambiar_password, name="cambiar_password"),

    # Logout propio del módulo: siempre redirige a Inicio
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="home"),
        name="logout",
    ),

    # =========================
    # ADMIN — Dashboard
    # =========================
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),

    # =========================
    # ADMIN — Usuarios
    # =========================
    path("admin/usuarios/", usuarios_lista, name="usuarios_lista"),
    path("admin/usuarios/nuevo/", usuarios_crear, name="usuarios_crear"),
    path("admin/usuarios/editar/<int:user_id>/", usuarios_editar, name="usuarios_editar"),
    path("admin/usuarios/eliminar/<int:user_id>/", usuarios_eliminar, name="usuarios_eliminar"),

    # =========================
    # ADMIN — Carreras
    # =========================
    path("admin/carreras/", carreras_lista, name="carreras_lista"),
    path("admin/carreras/<int:carrera_id>/", carrera_detalle, name="carrera_detalle"),
    path("admin/carreras/nueva/", crear_carrera, name="crear_carrera"),
    path("admin/carreras/editar/<int:carrera_id>/", carrera_editar, name="carrera_editar"),
    path("admin/carreras/eliminar/<int:carrera_id>/", carrera_eliminar, name="carrera_eliminar"),

    # =========================
    # ADMIN — Materias
    # =========================
    path("admin/materias/", materias_lista, name="materias_lista"),
    path("admin/materias/<int:materia_id>/", materia_detalle, name="materia_detalle"),
    path("admin/materias/nueva/", crear_materia, name="crear_materia"),
    path("admin/materias/editar/<int:materia_id>/", materia_editar, name="materia_editar"),
    path("admin/materias/eliminar/<int:materia_id>/", materia_eliminar, name="materia_eliminar"),

    # =========================
    # ADMIN — Cursadas / Asignaciones / Inscripciones
    # =========================
    path("admin/cursadas/", admin_cursadas, name="admin_cursadas"),
    path("admin/cursadas/<int:cursada_id>/", cursada_detalle, name="cursada_detalle"),
    path("admin/asignar-docente/", asignar_docente, name="asignar_docente"),
    path("admin/inscribir-alumnos/", inscribir_alumnos, name="inscribir_alumnos"),

    # =========================
    # ADMIN — Justificativos
    # =========================
    path("admin/justificativos/", lista_justificativos, name="lista_justificativos"),
    path("admin/justificativos/aprobar/<int:asistencia_id>/", aprobar_justificativo, name="aprobar_justificativo"),
    path("admin/justificativos/rechazar/<int:asistencia_id>/", rechazar_justificativo, name="rechazar_justificativo"),

    # =========================
    # ADMIN — Reportes
    # =========================
    path("admin/reportes/", reportes_curso, name="reportes_curso"),

    # =========================
    # MÉTRICAS (Admin / Docente / Alumno)
    # =========================
    path("admin/metricas/", admin_metricas, name="admin_metricas"),
    path("docente/metricas/", docente_metricas, name="docente_metricas"),
    path("alumno/metricas/", alumno_metricas, name="alumno_metricas"),

    # =========================
    # DOCENTE
    # =========================
    path("docente/dashboard/", docente_dashboard, name="docente_dashboard"),
    path("docente/cursos/", cursos_docente, name="cursos_docente"),
    path("docente/marcar/<int:curso_id>/", marcar_asistencia, name="marcar_asistencia"),
    
    # =========================
    # ALUMNO
    # =========================
    path("alumno/dashboard/", alumno_dashboard, name="alumno_dashboard"),
    path("alumno/asistencias/", consulta_asistencia, name="consulta_asistencia"),
    path("alumno/justificativo/subir/", subir_certificado, name="subir_certificado"),

    # =========================
    # Recuperación de contraseña
    # =========================
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
