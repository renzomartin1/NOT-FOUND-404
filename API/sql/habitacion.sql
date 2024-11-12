-- (para evitar errores si se vuelve a ejecutar el script (eliminar luego))
DROP TABLE IF EXISTS habitaciones;

-- Crear la tabla habitaciones
CREATE TABLE habitaciones (
    habitacion_id INT NOT NULL AUTO_INCREMENT,    
    hotel_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    precio INT NOT NULL,
    reservado BOOLEAN NOT NULL,
    capacidad int(11) NOT NULL
    PRIMARY KEY (habitacion_id),
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

ALTER TABLE habitaciones AUTO_INCREMENT = 30000;
