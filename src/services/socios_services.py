from src.repositories.socios_repository import (
    existe_socio_con_email,
    insertar_socio,
)
import re

class EmailDuplicadoError(Exception):
    pass

PATRON_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def email_valido(email: str) -> bool:
    return re.match(PATRON_EMAIL, email) is not None

def registrar_nuevo_socio(datos: dict) -> dict:
    nombre = datos.get("nombre")
    email = datos["email"].strip().lower()

    if not nombre:
        raise ValueError("El nombre esta vacio")
    
    if not email:
        raise ValueError("El email es obligatorio")


    if not email_valido(email):
        raise ValueError("El email no tiene un formato válido")

    if existe_socio_con_email(email):
        raise EmailDuplicadoError("El email ya esta registrado")

    id_socio = insertar_socio(nombre, email)

    return {
        "id": id_socio,
        "nombre": nombre,
        "email": email,
        "activo": True,
    }
