import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime, timedelta
import os
import csv

app = Flask(__name__)
minutos_por_turno = 15

# --- FUNCIONES PARA LA BD ---
def conectar_db():
    ruta = os.path.join(os.path.dirname(__file__), "turnos.db")
    return sqlite3.connect(ruta)

def inicializar_bd():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            especialidad TEXT,
            hora TEXT
        )
    """)
    conn.commit()
    conn.close()

def obtener_turnos(busqueda="", orden=""):
    conn = conectar_db()
    cursor = conn.cursor()
    query = "SELECT * FROM turnos"
    params = []

    if busqueda:
        query += " WHERE nombre LIKE ? OR especialidad LIKE ?"
        params.extend([f"%{busqueda}%", f"%{busqueda}%"])

    if orden == "hora":
        query += " ORDER BY hora"
    elif orden == "edad":
        query += " ORDER BY edad"

    cursor.execute(query, params)
    turnos = cursor.fetchall()
    conn.close()
    return turnos

def insertar_turno(nombre, edad, especialidad, hora):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO turnos (nombre, edad, especialidad, hora) VALUES (?, ?, ?, ?)",
                   (nombre, edad, especialidad, hora))
    conn.commit()
    conn.close()

# --- RUTAS ---
@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        edad = request.form.get("edad")
        hora = request.form.get("hora")
        minuto = request.form.get("minuto")
        editar_id = request.form.get("editar_id")

        if not nombre or not edad:
            error = "Nombre y edad son obligatorios."
        else:
            try:
                edad = int(edad)
                hora = int(hora) if hora else 0
                minuto = int(minuto) if minuto else 0
                if edad <= 0 or not (0 <= hora <= 23) or not (0 <= minuto <= 59):
                    raise ValueError
            except ValueError:
                error = "Datos inválidos."

        if not error:
            if edad < 15:
                especialidad = "Pediatría"
            elif 15 <= edad <= 59:
                especialidad = "Medicina General"
            else:
                especialidad = "Geriatría"

            hora_base = datetime.now().replace(hour=hora, minute=minuto, second=0, microsecond=0)
            turnos = obtener_turnos()
            if editar_id:
                cantidad_turnos = len(turnos) - 1
            else:
                cantidad_turnos = len(turnos)

            hora_turno = hora_base + timedelta(minutes=cantidad_turnos * minutos_por_turno)

            if editar_id:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE turnos
                    SET nombre = ?, edad = ?, especialidad = ?, hora = ?
                    WHERE id = ?
                """, (nombre, edad, especialidad, hora_turno.strftime("%H:%M"), editar_id))
                conn.commit()
                conn.close()
            else:
                insertar_turno(nombre, edad, especialidad, hora_turno.strftime("%H:%M"))

            return redirect(url_for("index"))

    # Obtener filtros y ordenar
    busqueda = request.args.get("busqueda", "").strip()
    orden = request.args.get("orden", "")
    turnos = obtener_turnos(busqueda, orden)

    return render_template("index.html", turnos=turnos, error=error)

@app.route("/descargar")
def descargar():
    ruta_csv = "turnos.csv"
    turnos = obtener_turnos()

    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Edad", "Especialidad", "Hora"])
        for t in turnos:
            writer.writerow(t[1:])

    return send_file(ruta_csv, as_attachment=True)

@app.route("/eliminar/<int:id>")
def eliminar_turno(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM turnos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/editar/<int:id>")
def editar(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turnos WHERE id = ?", (id,))
    turno = cursor.fetchone()
    conn.close()

    busqueda = request.args.get("busqueda", "")
    orden = request.args.get("orden", "")
    turnos = obtener_turnos(busqueda, orden)

    return render_template("index.html", turnos=turnos, turno_edit={
        "id": turno[0],
        "nombre": turno[1],
        "edad": turno[2],
        "especialidad": turno[3],
        "hora": turno[4]
    })

# --- EJECUCIÓN ---
inicializar_bd()

if __name__ == "__main__":
    app.run(debug=True)