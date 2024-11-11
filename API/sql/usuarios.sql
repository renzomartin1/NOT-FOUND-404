-- (para evitar errores si se vuelve a ejecutar el script (eliminar luego))
DROP TABLE IF EXISTS usuarios;

-- Crear la tabla usuarios
CREATE TABLE usuarios (
    usuario_id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    mail VARCHAR(100) NOT NULL,
    contraseña VARCHAR(100) NOT NULL,
    telefono INT NOT NULL,
    reserva_id INT NOT NULL,
    PRIMARY KEY (usuario_id),
    FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

ALTER TABLE usuarios AUTO_INCREMENT = 30000;
