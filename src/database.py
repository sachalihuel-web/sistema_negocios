import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


def conectar():

    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    return conexion


def crear_base_datos():

    conexion = conectar()

    cursor = conexion.cursor()

    # =====================================================
    # PRODUCTOS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre TEXT,
        stock INTEGER,
        precio REAL
    )
    """)

    # =====================================================
    # VENTAS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id SERIAL PRIMARY KEY,
        producto TEXT,
        cantidad INTEGER,
        total REAL,
        fecha TEXT
    )
    """)

    conexion.commit()

    conexion.close()
