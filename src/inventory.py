import sqlite3
import pandas as pd

def agregar_producto(nombre, stock, precio):

    conexion = sqlite3.connect("database/negocio.db")
    cursor = conexion.cursor()

    # Verificar si ya existe
    cursor.execute("""
    SELECT id
    FROM productos
    WHERE nombre = ?
    """, (nombre,))

    existe = cursor.fetchone()

    if existe:
        conexion.close()
        return False

    cursor.execute("""
    INSERT INTO productos (nombre, stock, precio)
    VALUES (?, ?, ?)
    """, (nombre, stock, precio))

    conexion.commit()
    conexion.close()

    return True


def obtener_productos():

    conexion = sqlite3.connect("database/negocio.db")

    df = pd.read_sql_query(
        "SELECT * FROM productos",
        conexion
    )

    conexion.close()

    return df
