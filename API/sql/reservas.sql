USE hospedajes;
CREATE TABLE IF NOT EXISTS reservas(
    id INT NOT NULL AUTO_INCREMENT,
    id_reserva INT NOT NULL,
    id_habitacion INT NOT NULL,
    fecha_entrada DATETIME,
    fecha_salida DATETIME,
    PRIMARY KEY (id)
);

INSERT INTO reservas (id_reserva,id_habitacion,fecha_entrada,fecha_salida)
VALUES (1234,12341234,'2024-2-23 00:00:00','2024-3-23 00:00:00');
INSERT INTO reservas (id_reserva,id_habitacion,fecha_entrada,fecha_salida)
VALUES (4567,45674567,'2024-3-23 00:00:00', '2024-4-23 00:00:00');