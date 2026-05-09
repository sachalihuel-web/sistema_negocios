import pandas as pd

from src.database import conectar


def agregar_producto(nombre, stock, precio):

    conexion = conectar()

    cursor = conexion.cursor()

    # ==========================================
    # VALIDAR SI EXISTE
    # ==========================================

    cursor.execute("""
    SELECT id
    FROM productos
    WHERE nombre = %s
    """, (nombre,))

    existe = cursor.fetchone()

    if existe:

        conexion.close()

        return False

    # ==========================================
    # INSERTAR
    # ==========================================

    cursor.execute("""
    INSERT INTO productos (
        nombre,
        stock,
        precio
    )
    VALUES (%s, %s, %s)
    """, (nombre, stock, precio))

    conexion.commit()

    conexion.close()

    return True


def obtener_productos():

    conexion = conectar()

    query = """
    SELECT *
    FROM productos
    """

    df = pd.read_sql(
        query,
        conexion
    )

    conexion.close()

    return df