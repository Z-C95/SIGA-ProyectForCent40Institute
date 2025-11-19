# asistencias/views/docente_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now

from ..models import Docente, DocenteMateria, AlumnoMateria, Asistencia
from ..permissions import is_docente


# ============================================================
# DASHBOARD DOCENTE
# ============================================================
@login_required
@user_passes_test(is_docente)
def docente_dashboard(request):
    """
    Panel principal del rol DOCENTE.
    Muestra un resumen de cursos, alumnos y asistencias.
    """
    docente = get_object_or_404(Docente, user=request.user)

    # Cursos asignados a este docente
    cursos = (
        DocenteMateria.objects
        .filter(docente=docente)
        .select_related("materia", "periodo", "docente")
    )
    total_cursos = cursos.count()

    # Alumnos totales (aproximado a partir de materia + periodo)
    am_qs = AlumnoMateria.objects.filter(
        materia__in=cursos.values("materia"),
        periodo__in=cursos.values("periodo"),
    )
    alumnos_totales = am_qs.values("alumno").distinct().count()

    # Registros de asistencia cargados por sus cursos
    asistencias_totales = Asistencia.objects.filter(
        alumno_materia__in=am_qs
    ).count()

    context = {
        "cursos": cursos,
        "total_cursos": total_cursos,
        "alumnos_totales": alumnos_totales,
        "asistencias_totales": asistencias_totales,
    }
    return render(request, "docente/dashboard.html", context)


# ============================================================
# LISTADO DE CURSOS DEL DOCENTE
# ============================================================
@login_required
@user_passes_test(is_docente)
def cursos_docente(request):
    """
    Lista las comisiones/cursos asignados al docente.
    """
    dm = (
        DocenteMateria.objects
        .filter(docente__user=request.user)
        .select_related("materia", "periodo", "docente")
    )
    return render(request, "docente/cursos.html", {"cursos": dm})


# ============================================================
# TOMAR / EDITAR ASISTENCIA PARA UN CURSO
# ============================================================
@login_required
@user_passes_test(is_docente)
def marcar_asistencia(request, curso_id):
    """
    Permite al docente registrar la asistencia de un curso (DocenteMateria)
    para una fecha determinada.
    """
    dm = get_object_or_404(
        DocenteMateria,
        id=curso_id,
        docente__user=request.user
    )

    # Inscripciones de alumnos a la materia/periodo de este curso
    inscriptos = (
        AlumnoMateria.objects
        .filter(materia=dm.materia, periodo=dm.periodo)
        .select_related("alumno")
    )

    # Fecha: si no viene en POST/GET, usamos hoy
    from datetime import date

    fecha_str = request.POST.get("fecha") or request.GET.get("fecha")
    if fecha_str:
        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            fecha = now().date()
    else:
        fecha = now().date()

    if request.method == "POST":
        # Guardar asistencia para cada alumno
        for am in inscriptos:
            estado = request.POST.get(f"estado_{am.id}", "Ausente")
            obs = request.POST.get(f"obs_{am.id}", "").strip()

            Asistencia.objects.update_or_create(
                alumno_materia=am,
                fecha=fecha,
                defaults={
                    "estado": estado,
                    "observaciones": obs,
                }
            )

        messages.success(request, "Asistencias registradas correctamente.")
        return redirect("asistencias:cursos_docente")

    # GET: construir estructura para la tabla
    alumnos = []
    for am in inscriptos:
        asistencia = Asistencia.objects.filter(
            alumno_materia=am,
            fecha=fecha
        ).first()
        alumnos.append({
            "alumno": am.alumno,
            "alumno_materia_id": am.id,
            "estado": asistencia.estado if asistencia else "Presente",
            "observaciones": asistencia.observaciones if asistencia else "",
        })

    context = {
        "curso": dm,
        "alumnos": alumnos,
        "fecha": fecha,
    }
    # Usa la plantilla "docente/marcar.html"
    return render(request, "docente/marcar.html", context)


# ============================================================
# MÉTRICAS DEL DOCENTE
# ============================================================
@login_required
@user_passes_test(is_docente)
def docente_metricas(request):
    """
    Métricas por curso para el docente.
    Muestra KPIs + detalle por curso con asistencia promedio y alumnos en riesgo.
    """
    docente = get_object_or_404(Docente, user=request.user)

    # Cursos asignados al docente
    cursos = (
        DocenteMateria.objects
        .filter(docente=docente)
        .select_related("materia", "periodo", "docente")
    )
    total_cursos = cursos.count()

    # Alumnos totales
    am_qs = AlumnoMateria.objects.filter(
        materia__in=cursos.values("materia"),
        periodo__in=cursos.values("periodo"),
    )
    alumnos_totales = am_qs.values("alumno").distinct().count()

    # Asistencias totales
    asistencias_totales = Asistencia.objects.filter(
        alumno_materia__in=am_qs
    ).count()

    # Detalle por curso
    detalle_cursos = []
    for c in cursos:
        am_curso = AlumnoMateria.objects.filter(
            materia=c.materia,
            periodo=c.periodo
        )
        asistencias = Asistencia.objects.filter(alumno_materia__in=am_curso)

        total = asistencias.count()
        if total:
            presentes = asistencias.filter(estado="Presente").count()
            justificados = asistencias.filter(estado="Justificado").count()
            porcentaje = round(((presentes + justificados) / total * 100), 2)
        else:
            porcentaje = 0

        # Alumnos en riesgo (< 75%)
        alumnos_riesgo = []
        for am in am_curso:
            a_qs = Asistencia.objects.filter(alumno_materia=am)
            t = a_qs.count()
            if not t:
                continue
            p = a_qs.filter(estado="Presente").count()
            j = a_qs.filter(estado="Justificado").count()
            porc_ind = round(((p + j) / t * 100), 2)
            if porc_ind < 75:
                alumnos_riesgo.append(am)

        detalle_cursos.append({
            "curso": c,
            "porcentaje": porcentaje,
            "alumnos_riesgo": alumnos_riesgo,
            "cant_riesgo": len(alumnos_riesgo),
        })

    context = {
        "total_cursos": total_cursos,
        "alumnos_totales": alumnos_totales,
        "asistencias_totales": asistencias_totales,
        "detalle_cursos": detalle_cursos,
    }
    return render(request, "docente/metricas.html", context)
