CREATE TABLE IF NOT EXISTS deportes (
    id  int AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS socios (
    id  int AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    email varchar(100) NOT NULL UNIQUE,
    activo boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS canchas (
    id  int AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    id_deporte int NOT NULL,
    precio_hora int NOT NULL,
    techada boolean NOT NULL DEFAULT false,
    activa boolean NOT NULL DEFAULT true,

    CONSTRAINT fk_canchas_deportes
        FOREIGN KEY (id_deporte)
        REFERENCES deportes(id)
);

CREATE TABLE IF NOT EXISTS reservas (
    id  int AUTO_INCREMENT PRIMARY KEY,
    id_socio int NOT NULL,
    id_cancha int NOT NULL,
    fecha_hora_inicio datetime(6) NOT NULL,
    fecha_hora_fin datetime(6) NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'finalizada') NOT NULL DEFAULT 'confirmada',
    precio_hora int NOT NULL,
    precio_total int NOT NULL,
    
    CONSTRAINT fk_reservas_socios
        FOREIGN KEY (id_socio)
        REFERENCES socios(id),

    CONSTRAINT fk_reservas_canchas
        FOREIGN KEY (id_cancha)
        REFERENCES canchas(id)
);

CREATE INDEX idx_reservas_cancha_fechas ON reservas (id_cancha, fecha_hora_inicio, fecha_hora_fin);
CREATE INDEX idx_reservas_socio_fechas ON reservas (id_socio, fecha_hora_inicio, fecha_hora_fin);

INSERT INTO deportes (nombre) VALUES 
('Fútbol'),
('Tenis'),
('Pádel');
