# SIGA - Sistema Integral de Gestión Académica

Sistema web desarrollado con Django 5 para la gestión de asistencias académicas del Instituto CENT N°40.

[![Deploy con Vercel](https://img.shields.io/badge/Deploy-Vercel-black?style=for-the-badge&logo=vercel)](https://siga-project-for-cent40-institute.vercel.app)
[![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue?style=for-the-badge&logo=postgresql)](https://neon.tech)

## 🚀 Demo en Vivo

**[Ver proyecto deployado](https://siga-project-for-cent40-institute.vercel.app)**

## 📋 Características

- ✅ Gestión de usuarios (docentes, alumnos)
- ✅ Control de asistencias
- ✅ Reportes estadísticos
- ✅ Sistema de autenticación
- ✅ Panel administrativo de Django

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 5.2
- **Base de datos:** PostgreSQL (Neon.tech)
- **Deploy:** Vercel
- **Almacenamiento estático:** WhiteNoise
- **Frontend:** HTML, CSS, JavaScript

## 📦 Instalación Local
```bash
# Clonar el repositorio
git clone https://github.com/Z-C95/SIGA-ProjectForCent40Institute.git
cd SIGA-ProjectForCent40Institute

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## 🌐 Deploy en Vercel

Este proyecto está configurado para deployarse automáticamente en Vercel:

1. Fork del repositorio
2. Importar en Vercel
3. Configurar variables de entorno:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `DEBUG=False`
4. Deploy automático

## 👥 Equipo de Desarrollo

Proyecto desarrollado por estudiantes avanzados de Análisis y Desarrollo de Sistemas Informáticos:
- Luis
- Érica
- Lautaro
- Gonzalo
- [Leandro.aka.ZC-95]

## 📄 Licencia

Instituto CENT N°40 - Campus Virtual Río Negro
