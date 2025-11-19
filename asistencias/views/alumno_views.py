# asistencias/views/alumno_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from ..models import Alumno, AlumnoMateria, Asistencia
from ..permissions import is_alumno


@login_required
@user_passes_test(is_alumno)
def alumno_dashboard(request):
    """
    Panel principal del rol ALUMNO.
    Muestra un resumen global de asistencia, materias activas,
    inasistencias y justificativos pendientes, además de materias en riesgo.
    """
    alumno = get_object_or_404(Alumno, user=request.user)

    # Todas las cursadas del alumno
    cursadas = (
        AlumnoMateria.objects
        .filter(alumno=alumno)
        .select_related("materia", "periodo")
    )

    # Todas las asistencias del alumno
    asistencias = (
        Asistencia.objects
        .filter(alumno_materia__alumno=alumno)
        .select_related("alumno_materia__materia", "alumno_materia__periodo")
    )

    # KPIs globales
    total_registros = asistencias.count()
    presentes = asistencias.filter(estado="Presente").count()
    justificados = asistencias.filter(estado="Justificado").count()
    ausentes = asistencias.filter(Q(estado="Ausente") | Q(estado="Tardanza")).count()

    if total_registros:
        porcentaje_global = round(((presentes + justificados) / total_registros * 100), 2)
    else:
        porcentaje_global = 0

    materias_activas = cursadas.count()

    # Justificados pendientes: estado "Justificado" pero sin validado_por
    justificativos_pendientes = asistencias.filter(
        estado="Justificado",
        validado_por__isnull=True
    ).count()

    # Materias en riesgo (< 75% de asistencia)
    materias_en_riesgo = []
    for am in cursadas:
        qs = asistencias.filter(alumno_materia=am)
        total = qs.count()
        if not total:
            continue
        pres = qs.filter(estado="Presente").count()
        jus = qs.filter(estado="Justificado").count()
        porcentaje = round(((pres + jus) / total * 100), 2)
        if porcentaje < 75:
            materias_en_riesgo.append({
                "cursada": am,
                "porcentaje": porcentaje,
            })

    context = {
        "porcentaje_global": porcentaje_global,
        "materias_activas": materias_activas,
        "ausentes_totales": ausentes,
        "justificados_pendientes": justificativos_pendientes,
        "materias_en_riesgo": materias_en_riesgo,
    }
    return render(request, "alumno/dashboard.html", context)


@login_required
@user_passes_test(is_alumno)
def consulta_asistencia(request):
    """
    Vista de 'Mis asistencias' para el alumno.
    Muestra tarjetas por materia con resumen + detalle expandible.
    """
    alumno = get_object_or_404(Alumno, user=request.user)

    cursadas = (
        AlumnoMateria.objects
        .filter(alumno=alumno)
        .select_related("materia", "periodo")
    )

    cursos = []
    for am in cursadas:
        qs = (
            Asistencia.objects
            .filter(alumno_materia=am)
            .order_by("fecha")
        )
        total = qs.count()
        if not total:
            continue

        presentes = qs.filter(estado="Presente").count()
        justificados = qs.filter(estado="Justificado").count()
        ausentes = qs.filter(Q(estado="Ausente") | Q(estado="Tardanza")).count()
        porcentaje = round(((presentes + justificados) / total * 100), 2) if total else 0

        cursos.append({
            "cursada": am,
            "total": total,
            "presentes": presentes,
            "justificados": justificados,
            "ausentes": ausentes,
            "porcentaje": porcentaje,
            "asistencias": qs,
        })

    context = {"cursos": cursos}
    return render(request, "alumno/consulta.html", context)


@login_required
@user_passes_test(is_alumno)
def subir_certificado(request):
    """
    Vista para subir certificados (justificativos).
    Muestra formulario y listado de justificativos cargados.
    """
    alumno = get_object_or_404(Alumno, user=request.user)
    cursadas = (
        AlumnoMateria.objects
        .filter(alumno=alumno)
        .select_related("materia", "periodo")
    )

    if request.method == "POST":
        am_id = request.POST.get("cursada")
        fecha = request.POST.get("fecha")
        archivo = request.FILES.get("certificado")

        if not (am_id and fecha and archivo):
            messages.error(request, "Faltan datos para subir el certificado.")
            return redirect("asistencias:subir_certificado")

        from django.core.files.storage import default_storage
        import uuid, os

        filename = f"{uuid.uuid4()}_{os.path.basename(archivo.name)}"
        path = default_storage.save(f"justificativos/{filename}", archivo)

        am = get_object_or_404(AlumnoMateria, id=am_id, alumno=alumno)

        a, _ = Asistencia.objects.get_or_create(
            alumno_materia=am,
            fecha=fecha,
            defaults={"estado": "Justificado"}
        )
        a.estado = "Justificado"
        a.justificativo_path = path
        a.save()

        messages.success(request, "Certificado subido correctamente. Queda pendiente de validación.")
        return redirect("asistencias:subir_certificado")

    justificativos = (
        Asistencia.objects
        .filter(alumno_materia__alumno=alumno, estado="Justificado")
        .select_related("alumno_materia__materia", "alumno_materia__periodo")
        .order_by("-fecha")
    )

    context = {
        "cursadas": cursadas,
        "justificativos": justificativos,
    }
    return render(request, "alumno/subir_certificado.html", context)


@login_required
@user_passes_test(is_alumno)
def alumno_metricas(request):
    """
    Métricas específicas del alumno por materia.
    Reutiliza la lógica de cálculo de porcentajes por cursada.
    """
    alumno = get_object_or_404(Alumno, user=request.user)

    cursadas = (
        AlumnoMateria.objects
        .filter(alumno=alumno)
        .select_related("materia", "periodo")
    )

    asistencias = (
        Asistencia.objects
        .filter(alumno_materia__alumno=alumno)
    )

    total_registros = asistencias.count()
    presentes = asistencias.filter(estado="Presente").count()
    justificados = asistencias.filter(estado="Justificado").count()
    ausentes = asistencias.filter(Q(estado="Ausente") | Q(estado="Tardanza")).count()

    if total_registros:
        porcentaje_global = round(((presentes + justificados) / total_registros * 100), 2)
    else:
        porcentaje_global = 0

    detalle_materias = []
    for am in cursadas:
        qs = asistencias.filter(alumno_materia=am)
        total = qs.count()
        if not total:
            continue
        pres = qs.filter(estado="Presente").count()
        jus = qs.filter(estado="Justificado").count()
        aus = qs.filter(Q(estado="Ausente") | Q(estado="Tardanza")).count()
        porcentaje = round(((pres + jus) / total * 100), 2)
        detalle_materias.append({
            "cursada": am,
            "total": total,
            "presentes": pres,
            "justificados": jus,
            "ausentes": aus,
            "porcentaje": porcentaje,
        })

    context = {
        "porcentaje_global": porcentaje_global,
        "materias_activas": cursadas.count(),
        "ausentes_totales": ausentes,
        "detalle_materias": detalle_materias,
    }
    return render(request, "alumno/metricas.html", context)
