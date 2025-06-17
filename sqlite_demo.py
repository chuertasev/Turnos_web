import sqlite3

# Conexión a la base de datos (se crea si no existe)
conexion = sqlite3.connect('turnos.db')
cursor = conexion.cursor()

# Crear la tabla
cursor.execute('''
CREATE TABLE IF NOT EXISTS turnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    especialidad TEXT,
    hora TEXT
)
''')

# Insertar un ejemplo
cursor.execute('''
INSERT INTO turnos (nombre, edad, especialidad, hora)
VALUES (?, ?, ?, ?)
''', ("Carlos", 31, "Medicina General", "18:30"))

# Guardar cambios y cerrar conexión
conexion.commit()
conexion.close()
print("Base de datos creada y registro insertado correctamente.")