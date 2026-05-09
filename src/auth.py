import os

from dotenv.main import load_dotenv

load_dotenv()

USUARIO = os.getenv("APP_USER")

PASSWORD = os.getenv("APP_PASSWORD")


def login(usuario, password):

    if usuario == USUARIO and password == PASSWORD:

        return True

    return False
