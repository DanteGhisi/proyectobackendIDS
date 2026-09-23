from src.db import ejecutar_consulta, ejecutar_mutacion


def existe_socio_con_email(email: str) -> bool:
    sql = """
        SELECT 1
        FROM socios
        WHERE email = :email
        LIMIT 1
    """

    resultado = ejecutar_consulta(sql, {"email": email})

    return bool(resultado)

def insertar_socio(nombre: str, email: str) -> int:
    sql = """
        INSERT INTO socios (nombre, email)
        VALUES (:nombre, :email)
        """

    parametros = {
        "nombre": nombre,
        "email": email,
    }

    return ejecutar_mutacion(sql, parametros)

    