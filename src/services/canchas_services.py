from src.repositories.canchas_repository import buscar_cancha_por_id_db, tiene_reservas_db, eliminar_cancha_db




def buscar_cancha_por_id(id: int) -> dict:
   if id <= 0:
       raise ValueError("El ID de la cancha debe ser positivo")


   cancha = buscar_cancha_por_id_db(id)
   if cancha is None:
       raise ValueError("La cancha no existe")


   return cancha




def eliminar_cancha(id: int):
   if id <= 0:
       raise ValueError("El ID de la cancha debe ser positivo")
   if tiene_reservas_db(id):
       raise ValueError("La cancha tiene reservas")
  
   id_cancha = eliminar_cancha_db(id)
   if id_cancha is None:
       raise ValueError("La cancha no existe")
  
