import pandas as pd
from datetime import datetime

from src.database import conectar


def registrar_venta(producto, cantidad, precio):

    total = cantidad * precio
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT stock
    FROM productos
    WHERE nombre = %s
    """, (producto,))

    resultado = cursor.fetchone()

    if resultado is None:
        conexion.close()
        return False

    stock_actual = resultado[0]

    if cantidad > stock_actual:
        conexion.close()
        return False

    cursor.execute("""
    INSERT INTO ventas (
        producto,
        cantidad,
        total,
        fecha
    )
    VALUES (%s, %s, %s, %s)
    """, (producto, cantidad, total, fecha))

    cursor.execute("""
    UPDATE productos
    SET stock = stock - %s
    WHERE nombre = %s
    """, (cantidad, producto))

    conexion.commit()
    conexion.close()

    return True


def obtener_ventas():

    conexion = conectar()

    query = """
    SELECT *
    FROM ventas
    """

    df = pd.read_sql(
        query,
        conexion
    )

    conexion.close()

    return df
