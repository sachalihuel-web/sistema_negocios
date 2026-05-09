import os
import streamlit as st
from dotenv.main import load_dotenv

load_dotenv()


def obtener_credenciales():

    usuario = st.secrets.get(
        "APP_USER",
        os.getenv("APP_USER")
    )

    password = st.secrets.get(
        "APP_PASSWORD",
        os.getenv("APP_PASSWORD")
    )

    return usuario, password


def login(usuario, password):

    usuario_correcto, password_correcto = obtener_credenciales()

    if usuario == usuario_correcto and password == password_correcto:
        return True

    return False
