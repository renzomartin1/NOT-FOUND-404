USE hospedajes;
DROP TABLE IF EXISTS reservaciones;
CREATE TABLE IF NOT EXISTS reservaciones (
    reserva_id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    hotel_id INT NOT NULL,
    habitacion_id INT NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    PRIMARY KEY (reserva_id),
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
            ON DELETE CASCADE
			ON UPDATE CASCADE,
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(habitacion_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);
ALTER TABLE reservaciones AUTO_INCREMENT = 40000;