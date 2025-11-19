# asistencias/views/alumno_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from ..models import Alumno, AlumnoMateria, Asistencia
from ..permissions import is_alumno

@login_required
@user_passes_test(is_alumno)
def consulta_asistencia(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    cursadas = (AlumnoMateria.objects
                .filter(alumno=alumno)
                .select_related("materia", "periodo"))

    resumen, detalle = [], []
    for am in cursadas:
        qs = Asistencia.objects.filter(alumno_materia=am)
        total = qs.count()
        presentes = qs.filter(estado="Presente").count()
        justificados = qs.filter(estado="Justificado").count()
        ausentes = qs.filter(Q(estado="Ausente") | Q(estado="Tardanza")).count()
        porcentaje = round(((presentes + justificados) / total * 100), 2) if total else 0
        resumen.append({
            "cursada": am, "total": total, "presentes": presentes,
            "justificados": justificados, "ausentes": ausentes, "porcentaje": porcentaje
        })
        for a in qs.order_by("fecha"):
            detalle.append(a)
    return render(request, "alumno/consulta.html", {"datos": resumen, "asistencias": detalle})

@login_required
@user_passes_test(is_alumno)
def subir_certificado(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    cursadas = (AlumnoMateria.objects
                .filter(alumno=alumno)
                .select_related("materia", "periodo"))

    if request.method == "POST":
        am_id = request.POST.get("cursada")
        fecha = request.POST.get("fecha")
        archivo = request.FILES.get("certificado")

        if not (am_id and fecha and archivo):
            messages.error(request, "Faltan datos.")
            return redirect("asistencias:subir_certificado")

        from django.core.files.storage import default_storage
        import uuid, os
        filename = f"{uuid.uuid4()}_{os.path.basename(archivo.name)}"
        path = default_storage.save(f"justificativos/{filename}", archivo)

        am = get_object_or_404(AlumnoMateria, id=am_id, alumno=alumno)

        a, _ = Asistencia.objects.get_or_create(
            alumno_materia=am, fecha=fecha, defaults={"estado": "Justificado"}
        )
        a.estado = "Justificado"
        a.justificativo_path = path
        a.save()
        messages.success(request, "Certificado subido correctamente.")
        return redirect("asistencias:subir_certificado")

    return render(request, "alumno/subir_certificado.html", {"cursadas": cursadas})
