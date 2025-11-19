# asistencias/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# ============================================================
# USER MANAGER
# ============================================================
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, rol="ALUMNO", **extra):
        if not username:
            raise ValueError("El username es obligatorio")
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, rol=rol, **extra)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra):
        extra.setdefault("is_active", True)
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)

        if not extra.get("is_staff"):
            raise ValueError("Superuser debe tener is_staff=True.")
        if not extra.get("is_superuser"):
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(username, email, password, rol="ADMIN", **extra)


# ============================================================
# USER CUSTOM
# ============================================================
class User(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrativo"
        DOCENTE = "DOCENTE", "Docente"
        ALUMNO = "ALUMNO", "Alumno"

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    rol = models.CharField(max_length=50, choices=Rol.choices, default=Rol.ALUMNO)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Avatar"
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["username"], name="idx_users_username"),
            models.Index(fields=["email"], name="idx_users_email"),
        ]

    def __str__(self):
        return f"{self.username} ({self.rol})"

# ============================================================
# ALUMNO
# ============================================================
class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    dni = models.IntegerField(unique=True)

    class Meta:
        db_table = "alumno"
        indexes = [
            models.Index(fields=["dni"], name="idx_alumno_dni")
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


# ============================================================
# DOCENTE
# ============================================================
class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    legajo = models.IntegerField(unique=True)

    class Meta:
        db_table = "docente"
        indexes = [
            models.Index(fields=["legajo"], name="idx_docente_legajo")
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


# ============================================================
# CARRERA
# ============================================================
class Carrera(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "carrera"

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


# ============================================================
# MATERIA
# ============================================================
class Materia(models.Model):
    nombre = models.CharField(max_length=200)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50)

    class Meta:
        db_table = "materia"
        constraints = [
            models.UniqueConstraint(
                fields=["codigo", "carrera"],
                name="unique_materia_carrera"
            )
        ]

    def __str__(self):
        return f"{self.nombre} - {self.carrera.codigo}/{self.codigo}"


# ============================================================
# PERIODO
# ============================================================
class Periodo(models.Model):
    id = models.IntegerField(primary_key=True, help_text="AAAAMM, ej: 202401")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=False)

    class Meta:
        db_table = "periodo"
        indexes = [
            models.Index(fields=["activo"], name="idx_periodo_activo")
        ]

    def __str__(self):
        return f"{self.id} ({'Activo' if self.activo else 'Inactivo'})"

    @property
    def nombre(self):
        return str(self.id)


# ============================================================
# DOCENTE - MATERIA - PERIODO
# ============================================================
class DocenteMateria(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    turno = models.CharField(max_length=50, null=True, blank=True)
    aula = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "docente_materia"
        constraints = [
            models.UniqueConstraint(
                fields=["docente", "materia", "periodo"],
                name="unique_docente_materia_periodo"
            )
        ]
        indexes = [
            models.Index(fields=["periodo"], name="idx_docente_materia_periodo")
        ]

    def __str__(self):
        return f"{self.materia} - {self.docente} - {self.periodo_id}"


# ============================================================
# ALUMNO - MATERIA - PERIODO
# ============================================================
class AlumnoMateria(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado_inscripcion = models.CharField(max_length=50, default="Activo")

    class Meta:
        db_table = "alumno_materia"
        constraints = [
            models.UniqueConstraint(
                fields=["alumno", "materia", "periodo"],
                name="unique_alumno_materia_periodo"
            )
        ]
        indexes = [
            models.Index(fields=["alumno"], name="idx_alumno_materia_alumno")
        ]

    def __str__(self):
        return f"{self.alumno} -> {self.materia} [{self.periodo_id}]"


# ============================================================
# ASISTENCIA
# ============================================================
class Asistencia(models.Model):
    ESTADOS = (
        ("Presente", "Presente"),
        ("Ausente", "Ausente"),
        ("Tardanza", "Tardanza"),
        ("Justificado", "Justificado"),
    )

    alumno_materia = models.ForeignKey(AlumnoMateria, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS)

    justificativo_path = models.CharField(max_length=255, null=True, blank=True)
    validado_por = models.ForeignKey(Docente, null=True, blank=True, on_delete=models.SET_NULL)
    validado_fecha = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "asistencia"
        constraints = [
            models.UniqueConstraint(
                fields=["alumno_materia", "fecha"],
                name="unique_asistencia_fecha"
            )
        ]
        indexes = [
            models.Index(fields=["fecha"], name="idx_asistencia_fecha"),
            models.Index(fields=["alumno_materia"], name="idx_asistencia_alumno_materia"),
        ]

    def __str__(self):
        return f"{self.alumno_materia} - {self.fecha} ({self.estado})"

    @property
    def cuenta_como_presente(self):
        return self.estado in ("Presente", "Justificado")
