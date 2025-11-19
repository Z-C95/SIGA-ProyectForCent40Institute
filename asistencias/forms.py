from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import (
    User, Alumno, Docente, Carrera, Materia, Periodo,
    DocenteMateria, AlumnoMateria
)

# ========================
# Usuarios
# ========================
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repetir contraseña"}),
        label="Repetir contraseña"
    )

    class Meta:
        model = User
        fields = ("username", "email", "rol", "is_active", "is_staff")
        labels = {
            "username": "Usuario",
            "email": "Correo electrónico",
            "rol": "Rol",
            "is_active": "Activo",
            "is_staff": "Staff (acceso al admin)",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "usuario"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@dominio.com"}),
            "rol": forms.Select(choices=User.Rol.choices, attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Ya existe un usuario con ese correo.")
        return email

    def clean_password1(self):
        pwd = self.cleaned_data.get("password1")
        validate_password(pwd)
        return pwd

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserEditForm(forms.ModelForm):
    # Campos opcionales para que el ADMIN pueda cambiar la contraseña
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        required=False,
        help_text="Dejar en blanco si no querés cambiar la contraseña.",
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        required=False,
    )

    class Meta:
        model = User
        fields = ["username", "email", "rol", "is_active", "is_staff", "is_superuser"]
        labels = {
            "username": "Usuario",
            "email": "Correo electrónico",
            "rol": "Rol",
            "is_active": "Activo",
            "is_staff": "Staff (acceso al admin)",
            "is_superuser": "Superusuario",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rol": forms.Select(choices=User.Rol.choices, attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_superuser": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe un usuario con ese correo.")
        return email

    def clean_new_password1(self):
        """
        Valida la nueva contraseña sólo si el admin escribió algo.
        """
        pwd = self.cleaned_data.get("new_password1")
        if pwd:
            # Usa las validaciones de Django, teniendo en cuenta al usuario
            validate_password(pwd, user=self.instance)
        return pwd

    def clean(self):
        cleaned = super().clean()
        pwd1 = cleaned.get("new_password1")
        pwd2 = cleaned.get("new_password2")

        # Si uno de los dos campos está cargado, verificamos que coincidan
        if pwd1 or pwd2:
            if pwd1 != pwd2:
                self.add_error("new_password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        """
        Guarda los datos del usuario y, si se indicó una nueva contraseña,
        la actualiza usando set_password().
        """
        user = super().save(commit=False)

        new_password = self.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user


# ================================
# Admin: Carreras y Materias
# ================================
class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ["nombre", "codigo"]
        labels = {"nombre": "Nombre", "codigo": "Código"}
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de la carrera"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código (ej.: TDS)"}),
        }

    def clean_codigo(self):
        codigo = (self.cleaned_data["codigo"] or "").strip()
        if Carrera.objects.filter(codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe una carrera con ese código.")
        return codigo

    def clean_nombre(self):
        nombre = (self.cleaned_data["nombre"] or "").strip()
        if Carrera.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe una carrera con ese nombre.")
        return nombre


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ["nombre", "codigo", "carrera"]
        labels = {"nombre": "Nombre", "codigo": "Código", "carrera": "Carrera"}
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de la materia"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código (ej.: PROG1)"}),
            "carrera": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar el desplegable de carreras alfabéticamente
        self.fields["carrera"].queryset = Carrera.objects.order_by("nombre")

    def clean(self):
        cleaned = super().clean()
        nombre = (cleaned.get("nombre") or "").strip()
        codigo = (cleaned.get("codigo") or "").strip()
        carrera = cleaned.get("carrera")

        # Unicidad por (carrera, código) y (carrera, nombre) para evitar duplicados
        if carrera and codigo:
            if Materia.objects.filter(carrera=carrera, codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
                self.add_error("codigo", "Ya existe una materia en esta carrera con ese código.")
        if carrera and nombre:
            if Materia.objects.filter(carrera=carrera, nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
                self.add_error("nombre", "Ya existe una materia en esta carrera con ese nombre.")
        return cleaned


# ================================
# Admin: Asignación Docente y Alta de Alumnos en Materia/Periodo
# ================================
class DocenteMateriaForm(forms.ModelForm):
    class Meta:
        model = DocenteMateria
        fields = ("docente", "materia", "periodo")
        labels = {"docente": "Docente", "materia": "Materia", "periodo": "Periodo"}
        widgets = {
            "docente": forms.Select(attrs={"class": "form-select"}),
            "materia": forms.Select(attrs={"class": "form-select"}),
            "periodo": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["docente"].queryset = Docente.objects.select_related("user").order_by("apellido", "nombre")
        self.fields["materia"].queryset = Materia.objects.order_by("nombre")
        self.fields["periodo"].queryset = Periodo.objects.order_by("id")

    def clean(self):
        cleaned = super().clean()
        docente = cleaned.get("docente")
        materia = cleaned.get("materia")
        periodo = cleaned.get("periodo")
        if docente and materia and periodo:
            if DocenteMateria.objects.filter(docente=docente, materia=materia, periodo=periodo).exists():
                raise forms.ValidationError("Ya existe una asignación de ese docente para esa materia y periodo.")
        return cleaned


class AlumnoMateriaForm(forms.Form):
    materia = forms.ModelChoiceField(
        queryset=Materia.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Materia"
    )
    periodo = forms.ModelChoiceField(
        queryset=Periodo.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Periodo"
    )
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 12}),
        label="Alumnos"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["materia"].queryset = Materia.objects.order_by("nombre")
        self.fields["periodo"].queryset = Periodo.objects.order_by("id")
        self.fields["alumnos"].queryset = Alumno.objects.order_by("apellido", "nombre")


# ================================
# Formularios de PERFIL (User / Docente / Alumno)
# ================================
class PerfilUserForm(forms.ModelForm):
    """Formulario para que el usuario actualice su email y avatar."""
    class Meta:
        model = User
        fields = ["email", "avatar"]
        labels = {
            "email": "Correo electrónico",
            "avatar": "Avatar",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class PerfilDocenteForm(forms.ModelForm):
    """Formulario para que el DOCENTE actualice sus datos personales."""
    class Meta:
        model = Docente
        # Campos que existen en Docente
        fields = ["nombre", "apellido", "legajo"]
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "legajo": "Legajo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "legajo": forms.NumberInput(attrs={"class": "form-control"}),
        }


class PerfilAlumnoForm(forms.ModelForm):
    """Formulario para que el ALUMNO actualice sus datos personales."""
    class Meta:
        model = Alumno
        # Campos que existen en Alumno
        fields = ["nombre", "apellido", "dni"]
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "dni": "DNI",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "dni": forms.NumberInput(attrs={"class": "form-control"}),
        }
