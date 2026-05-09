import sqlite3

def crear_base_datos():

    conexion = sqlite3.connect("database/negocio.db")

    cursor = conexion.cursor()

    # 📦 Tabla productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        stock INTEGER,
        precio REAL
    )
    """)

    # 💰 Tabla ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        cantidad INTEGER,
        total REAL,
        fecha TEXT    )
    """)

    conexion.commit()
    conexion.close()
