-- Parte de la copia de seguridad por si queremos restablecer la base de datos "hospedajes".
DROP TABLE IF EXISTS usuarios;

-- Creación de la tabla "usuarios".
CREATE TABLE usuarios (
	usuario_id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contraseña VARCHAR(75) NOT NULL,
    telefono INT NOT NULL,
    PRIMARY KEY (usuario_id)
);

-- Modificación de la tabla "usuarios" para que la columna "usuario_id" comience desde 10000 en adelante.
ALTER TABLE usuarios AUTO_INCREMENT = 10000;
