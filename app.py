import csv
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from flask import send_file
import os

app = Flask(__name__)
turnos = []
espera_total = 1 * 15  # 5 personas antes x 15 minutos
minutos_por_turno = 15

@app.route("/", methods=["GET", "POST"])
def index():
    global espera_total

    error = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        edad = request.form.get("edad")
        hora = request.form.get("hora")
        minuto = request.form.get("minuto")
        editar_index = request.form.get("editar_index")

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

            if editar_index and editar_index.isdigit():
                index = int(editar_index)
                nueva_hora = hora_base + timedelta(minutes=index * minutos_por_turno)

                turnos[index] = {
                    "nombre": nombre,
                    "edad": edad,
                    "especialidad": especialidad,
                    "hora": nueva_hora.strftime("%H:%M")
                }
            else:
                hora_turno = hora_base + timedelta(minutes=espera_total)
                espera_total += minutos_por_turno

                nuevo_turno = {
                    "nombre": nombre,
                    "edad": edad,
                    "especialidad": especialidad,
                    "hora": hora_turno.strftime("%H:%M")
                }

                turnos.append(nuevo_turno)

            guardar_en_csv_completo()
            return redirect(url_for("index"))

    return render_template("index.html", turnos=turnos, error=error)

def guardar_en_csv_completo():
    ruta_absoluta = os.path.join(os.path.dirname(__file__), "turnos.csv")
    with open(ruta_absoluta, "w", newline="", encoding="utf-8") as f:
        campos = ["nombre", "edad", "especialidad", "hora"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for t in turnos:
            writer.writerow(t)

@app.route("/eliminar/<int:index>")
def eliminar(index):
    if 0 <= index < len(turnos):
        turnos.pop(index)
        guardar_en_csv_completo()
    return redirect(url_for("index"))

@app.route("/editar/<int:index>")
def editar(index):
    if 0 <= index < len(turnos):
        turno = turnos[index]
        return render_template("index.html", turnos=turnos, editar=turno, index=index)
    return redirect(url_for("index"))

@app.route("/descargar")
def descargar():
    ruta_csv = os.path.join(os.path.dirname(__file__), "turnos.csv")
    return send_file(ruta_csv, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)