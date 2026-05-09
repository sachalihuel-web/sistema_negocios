import os
import psycopg2
import streamlit as st

from dotenv import load_dotenv

load_dotenv()


def obtener_config(nombre, valor_default=None):
    try:
        return st.secrets.get(nombre, valor_default)
    except Exception:
        return valor_default


def conectar():

    host = obtener_config("DB_HOST", os.getenv("DB_HOST"))
    database = obtener_config("DB_NAME", os.getenv("DB_NAME"))
    user = obtener_config("DB_USER", os.getenv("DB_USER"))
    password = obtener_config("DB_PASSWORD", os.getenv("DB_PASSWORD"))
    port = obtener_config("DB_PORT", os.getenv("DB_PORT"))

    conexion = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
        sslmode="require"
    )

    return conexion


def crear_base_datos():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre TEXT UNIQUE,
        stock INTEGER,
        precio REAL
    )
    """)

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