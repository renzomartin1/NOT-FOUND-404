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
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(habitacion_id)
);

INSERT INTO reservaciones (usuario_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida)
VALUES (2001,02,'9-B','2024-2-23 00:00:00','2024-3-23 00:00:00');
INSERT INTO reservaciones (usuario_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida)
VALUES (2002,07,'17-A','2024-3-23 00:00:00', '2024-4-23 00:00:00');