USE hospedajes;
DROP TABLE IF EXISTS reservaciones;
CREATE TABLE IF NOT EXISTS reservaciones(
    id INT NOT NULL AUTO_INCREMENT,
    reserva_id INT NOT NULL,
    usuario_id INT NOT NULL,
    hotel_id INT NOT NULL,
    habitacion_id VARCHAR(100),
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    PRIMARY KEY (id, reserva_id)
);

INSERT INTO reservaciones (reserva_id, usuario_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida)
VALUES (1234,2001,02,'9-B','2024-2-23 00:00:00','2024-3-23 00:00:00');
INSERT INTO reservaciones (reserva_id, usuario_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida)
VALUES (4567,2002,07,'17-A','2024-3-23 00:00:00', '2024-4-23 00:00:00');