# Turnos_web

Sistema de gestión de turnos médicos desarrollado en Flask.

## 📋 Descripción

Esta aplicación permite registrar pacientes, calcular la hora estimada de atención según el orden de llegada y especialidad, editar turnos, eliminarlos y descargar un archivo CSV con todos los registros.

Fue desarrollada por Carlos como parte de una ruta de aprendizaje técnico personalizada, y desplegada exitosamente en PythonAnywhere.

## 🚀 Funcionalidades

- Registro de pacientes con nombre, edad y hora de llegada.
- Asignación automática de especialidad:
  - < 15 años: Pediatría
  - 15–59 años: Medicina General
  - 60+ años: Geriatría
- Cálculo automático de hora estimada (5 turnos antes x 15 min).
- Edición y eliminación de turnos.
- Descarga de registros en CSV.
- Interfaz web responsive (HTML + Jinja2).

## 🛠 Tecnologías

- Python 3
- Flask
- HTML5 + CSS3
- Git & GitHub
- PythonAnywhere

## 📦 Instalación local

1. Clona el repositorio:

```bash
git clone https://github.com/chuertasev/Turnos_web.git
cd Turnos_web
```

2. Instala Flask:

```bash
pip install flask
```

3. Ejecuta la app:

```bash
python app.py
```

4. Abre en el navegador:  
`http://localhost:5000`

## 🌐 Sitio en producción

La aplicación está desplegada y disponible en:  
👉 https://chuertasev.pythonanywhere.com/

## 📄 Licencia

Este proyecto fue desarrollado como parte del aprendizaje de Carlos Huerta con apoyo de su sensei digital (ChatGPT). Puedes reutilizarlo con fines educativos y personales.

---

_Última actualización: 17/06/2025_