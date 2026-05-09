import sqlite3
import pandas as pd
from datetime import datetime


def registrar_venta(producto, cantidad, precio):

    total = cantidad * precio

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    conexion = sqlite3.connect("database/negocio.db")

    cursor = conexion.cursor()

    # 🔍 Verificar stock actual
    cursor.execute("""
    SELECT stock
    FROM productos
    WHERE nombre = ?
    """, (producto,))

    resultado = cursor.fetchone()

    if resultado is None:
        conexion.close()
        return False

    stock_actual = resultado[0]

    # ❌ Validar stock
    if cantidad > stock_actual:
        conexion.close()
        return False

    # 💰 Registrar venta
    cursor.execute("""
    INSERT INTO ventas (producto, cantidad, total, fecha)
    VALUES (?, ?, ?, ?)
    """, (producto, cantidad, total, fecha))

    # 📦 Actualizar stock
    cursor.execute("""
    UPDATE productos
    SET stock = stock - ?
    WHERE nombre = ?
    """, (cantidad, producto))

    conexion.commit()

    conexion.close()

    return True


def obtener_ventas():

    conexion = sqlite3.connect("database/negocio.db")

    df = pd.read_sql_query(
        "SELECT * FROM ventas",
        conexion
    )

    conexion.close()

    return df
