# asistencias/views/general_views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from ..models import User, Docente, Alumno
from ..forms import (
    PerfilUserForm,
    PerfilDocenteForm,
    PerfilAlumnoForm,
)


# asistencias/views/general_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Redirecciones según rol
    if getattr(request.user, "rol", None) == "ADMIN":
        # ADMIN → Dashboard
        return redirect("asistencias:admin_dashboard")

    if getattr(request.user, "rol", None) == "DOCENTE":
        # DOCENTE → cursos del docente
        return redirect("asistencias:docente_dashboard")

    if getattr(request.user, "rol", None) == "ALUMNO":
        # ALUMNO → vista de asistencias
        return redirect("asistencias:alumno_dashboard")

    # Por si hay algún usuario sin rol definido
    return render(request, "home.html")

# ============================================================
# PERFIL: actualización de datos del usuario (docente/alumno)
# ============================================================
@login_required
def editar_perfil(request):
    """
    Permite editar:
      - Email y avatar del usuario
      - Datos personales del docente o alumno
    No permite edición para administradores sin perfil asociado.
    """
    user = request.user
    docente = getattr(user, "docente", None)
    alumno = getattr(user, "alumno", None)

    # Solo docentes o alumnos pueden editar perfil
    if not docente and not alumno:
        messages.error(request, "Solo los docentes y alumnos pueden editar su perfil.")
        return redirect("asistencias:home")

    if request.method == "POST":
        user_form = PerfilUserForm(request.POST, request.FILES, instance=user)
        docente_form = PerfilDocenteForm(request.POST, instance=docente) if docente else None
        alumno_form = PerfilAlumnoForm(request.POST, instance=alumno) if alumno else None

        valid = user_form.is_valid()
        if docente_form:
            valid = valid and docente_form.is_valid()
        if alumno_form:
            valid = valid and alumno_form.is_valid()

        if valid:
            user_form.save()
            if docente_form:
                docente_form.save()
            if alumno_form:
                alumno_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("asistencias:editar_perfil")
        else:
            messages.error(request, "Revisá los datos del formulario.")
    else:
        user_form = PerfilUserForm(instance=user)
        docente_form = PerfilDocenteForm(instance=docente) if docente else None
        alumno_form = PerfilAlumnoForm(instance=alumno) if alumno else None

    context = {
        "user_form": user_form,
        "docente_form": docente_form,
        "alumno_form": alumno_form,
    }
    return render(request, "perfil/editar_perfil.html", context)


# ============================================================
# CAMBIAR CONTRASEÑA (ALUMNO / DOCENTE)
# ============================================================
@login_required
def cambiar_password(request):
    """
    Permite al usuario cambiar su contraseña actual.
    Mantiene la sesión activa después del cambio.
    """
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect("asistencias:editar_perfil")
        else:
            messages.error(request, "Revisá los datos del formulario.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "perfil/cambiar_password.html", {"form": form})
