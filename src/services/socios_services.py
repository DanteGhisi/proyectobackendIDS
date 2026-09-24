from src.repositories.socios_repository import (
    existe_socio_con_email,
    insertar_socio,
    obtener_todos_los_socios_db,
    buscar_socio_por_id_db,
    actualizar_socio_db,
)
from src.db import ejecutar_consulta
import re

PATRON_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def email_valido(email: str) -> bool:
    return re.match(PATRON_EMAIL, email) is not None

def registrar_nuevo_socio(datos: dict) -> dict:
    if not isinstance(datos, dict):
        raise ValueError("El cuerpo de la solicitud debe ser un JSON válido")
        
    nombre = datos.get("nombre")
    email = datos.get("email")

    if not nombre or not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre esta vacio")
    
    if not email or not isinstance(email, str):
        raise ValueError("El email es obligatorio")

    email = email.strip().lower()
    if not email_valido(email):
        raise ValueError("El email no tiene un formato válido")

    if existe_socio_con_email(email):
        raise ValueError("El email ya esta registrado")

    id_socio = insertar_socio(nombre.strip(), email)
    return buscar_socio_por_id_db(id_socio)

def obtener_todos_los_socios(nombre=None, activo=None, limit=10, offset=0):
    return obtener_todos_los_socios_db(nombre=nombre, activo=activo, limit=limit, offset=offset)

def buscar_socio_por_id(id: int):
    socio = buscar_socio_por_id_db(id)
    if not socio:
        raise ValueError("El socio no existe")
    return socio

def modificar_socio(id: int, datos: dict) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ValueError("El cuerpo de la solicitud debe ser un JSON válido")

    permitidos = {"nombre", "email", "activo"}
    desconocidos = set(datos.keys()) - permitidos
    if desconocidos:
        raise ValueError(f"Campos desconocidos: {', '.join(sorted(desconocidos))}")

    socio_actual = buscar_socio_por_id_db(id)
    if not socio_actual:
        raise ValueError("El socio no existe")

    updates = []
    params = {"id": id}

    if "nombre" in datos:
        nombre = datos["nombre"]
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        updates.append("nombre = :nombre")
        params["nombre"] = nombre.strip()

    if "email" in datos:
        email = datos["email"]
        if not isinstance(email, str):
            raise ValueError("El email debe ser un texto")
        
        email = email.strip().lower()
        if not email_valido(email):
            raise ValueError("El email no tiene un formato válido")

        duplicado = ejecutar_consulta("SELECT id FROM socios WHERE email = :email AND id != :id", {"email": email, "id": id})
        if duplicado:
            raise ValueError("El email ya esta registrado")

        updates.append("email = :email")
        params["email"] = email

    if "activo" in datos:
        activo = datos["activo"]
        if not isinstance(activo, bool):
            raise ValueError("El campo activo debe ser true o false")
        updates.append("activo = :activo")
        params["activo"] = activo

    if not updates:
        raise ValueError("No se proporcionaron campos para actualizar")

    actualizar_socio_db(id, updates, params)
    return buscar_socio_por_id_db(id)