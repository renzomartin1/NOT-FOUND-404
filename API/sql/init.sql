CREATE DATABASE hospedajes;

USE hospedajes;

DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    usuario_id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contraseña VARCHAR(75) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    PRIMARY KEY (usuario_id)
);

ALTER TABLE usuarios AUTO_INCREMENT = 10000;

DROP TABLE IF EXISTS hoteles;

CREATE TABLE hoteles (   
    hotel_id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    barrio VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    servicios VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (hotel_id)
);

ALTER TABLE hoteles AUTO_INCREMENT = 30000;

DROP TABLE IF EXISTS habitaciones;

CREATE TABLE habitaciones (
    habitacion_id INT NOT NULL AUTO_INCREMENT,    
    hotel_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    precio INT NOT NULL,
    capacidad INT NOT NULL,
    calificacion INT NOT NULL,
    PRIMARY KEY (habitacion_id),
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

ALTER TABLE habitaciones AUTO_INCREMENT = 20000;

DROP TABLE IF EXISTS reservaciones;
CREATE TABLE IF NOT EXISTS reservaciones (
    reserva_id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    hotel_id INT NOT NULL,
    habitacion_id INT NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    PRIMARY KEY (reserva_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
        ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
        ON DELETE CASCADE
	    ON UPDATE CASCADE,
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(habitacion_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);
ALTER TABLE reservaciones AUTO_INCREMENT = 40000;
