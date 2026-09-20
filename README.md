Ejecución de base de datos:

```bash
# 1. Crear la base de datos si no existe
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS club_deportivo_db;"

# 2. Ejecutar el script SQL para crear las tablas
mysql -u root -p club_deportivo_db < db/init_db.sql
```