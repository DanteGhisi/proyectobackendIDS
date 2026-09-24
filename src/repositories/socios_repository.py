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

def obtener_todos_los_socios_db(nombre=None, activo=None, limit=10, offset=0):
    base_query = "FROM socios WHERE 1=1"
    params = {}
    
    if nombre:
        base_query += " AND nombre LIKE :nombre"
        params["nombre"] = f"%{nombre}%"
        
    if activo is not None:
        base_query += " AND activo = :activo"
        params["activo"] = activo
        
    res_total = ejecutar_consulta(f"SELECT COUNT(*) AS total {base_query}", params)
    total = res_total[0]['total'] if res_total else 0

    query = f"SELECT id, nombre, email, activo {base_query} ORDER BY id ASC LIMIT :limite OFFSET :offset"
    params_data = params.copy()
    params_data["limite"] = limit
    params_data["offset"] = offset
    
    socios = ejecutar_consulta(query, params_data)
    
    # convertimos activo a booleano real
    for socio in socios:
        socio["activo"] = bool(socio["activo"])
        
    return socios, total

def buscar_socio_por_id_db(id: int):
    query = "SELECT id, nombre, email, activo FROM socios WHERE id = :id"
    resultado = ejecutar_consulta(query, {"id": id})
    if resultado:
        socio = resultado[0]
        socio["activo"] = bool(socio["activo"])
        return socio
    return None

def actualizar_socio_db(id: int, updates: list, params: dict):
    query = f"UPDATE socios SET {', '.join(updates)} WHERE id = :id"
    ejecutar_mutacion(query, params)