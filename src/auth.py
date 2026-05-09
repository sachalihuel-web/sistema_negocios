import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def obtener_secret(nombre, valor_default=None):
    try:
        return st.secrets.get(nombre, valor_default)
    except Exception:
        return valor_default


def obtener_credenciales():

    usuario = obtener_secret(
        "APP_USER",
        os.getenv("APP_USER")
    )

    password = obtener_secret(
        "APP_PASSWORD",
        os.getenv("APP_PASSWORD")
    )

    return usuario, password


def login(usuario, password):

    usuario_correcto, password_correcto = obtener_credenciales()

    if usuario == usuario_correcto and password == password_correcto:
        return True

    return False

