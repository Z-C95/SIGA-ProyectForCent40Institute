# asistencias/views/docente_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now

from ..models import DocenteMateria, AlumnoMateria, Asistencia
from ..permissions import is_docente

@login_required
@user_passes_test(is_docente)
def cursos_docente(request):
    dm = (DocenteMateria.objects
          .filter(docente__user=request.user)
          .select_related("materia", "periodo", "docente"))
    return render(request, "docente/cursos.html", {"cursos": dm})

@login_required
@user_passes_test(is_docente)
def marcar_asistencia(request, curso_id):
    dm = get_object_or_404(DocenteMateria, id=curso_id, docente__user=request.user)
    inscriptos = (AlumnoMateria.objects
                  .filter(materia=dm.materia, periodo=dm.periodo)
                  .select_related("alumno"))

    if request.method == "POST":
        fecha = now().date()
        for am in inscriptos:
            estado = request.POST.get(f"alumno_{am.alumno.id}", "Ausente")
            Asistencia.objects.update_or_create(
                alumno_materia=am,
                fecha=fecha,
                defaults={"estado": estado}
            )
        messages.success(request, "Asistencias registradas correctamente.")
        return redirect("asistencias:cursos_docente")

    alumnos = [am.alumno for am in inscriptos]
    return render(request, "docente/marcar.html", {"curso": dm, "alumnos": alumnos})
