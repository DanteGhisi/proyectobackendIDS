from src.db import ejecutar_consulta, ejecutar_mutacion




def buscar_cancha_por_id_db(id: int):
   query = """
       SELECT id, nombre, id_deporte, precio_hora, techada, activa
       FROM canchas
       WHERE id = :id
   """
   resultado = ejecutar_consulta(query, {"id": id})
   if not resultado:
       return None


   cancha = resultado[0]
   cancha["techada"] = bool(cancha["techada"])
   cancha["activa"] = bool(cancha["activa"])


   return cancha


def tiene_reservas_db(id: int) -> bool:
   query = """
           SELECT id_cancha
           FROM reservas
           WHERE id_cancha = :id
       """
   resultado = (ejecutar_consulta(query, {"id": id}))
   if resultado:
       return True
   else:
       return False


def eliminar_cancha_db (id: int) -> int:
   sql = "DELETE FROM canchas WHERE id = :id"
   parametros = {
           "id": id,
       }
   return ejecutar_mutacion(sql, parametros)
