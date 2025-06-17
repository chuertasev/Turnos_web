import sqlite3

# Conectarse a la base de datos existente
conexion = sqlite3.connect('turnos.db')
cursor = conexion.cursor()

# Leer todos los registros
cursor.execute("SELECT * FROM turnos WHERE edad >= 18")
turnos = cursor.fetchall()

# Mostrar resultados
print("Turnos registrados:")
print("-------------------")
for turno in turnos:
    print(f"ID: {turno[0]} | Nombre: {turno[1]} | Edad: {turno[2]} | Especialidad: {turno[3]} | Hora: {turno[4]}")

# Cerrar conexión
conexion.close()