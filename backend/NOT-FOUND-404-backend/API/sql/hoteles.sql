-- (para evitar errores si se vuelve a ejecutar el script (eliminar luego))
DROP TABLE IF EXISTS hoteles;

-- Crear la tabla hoteles
CREATE TABLE hoteles (   
    hotel_id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    barrio VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    servicios VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    imagen_principal VARCHAR(200) NOT NULL,
    puntuacion INT NOT NULL,
    PRIMARY KEY (hotel_id)
);

ALTER TABLE hoteles AUTO_INCREMENT = 30000;

