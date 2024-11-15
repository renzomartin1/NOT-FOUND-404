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
    PRIMARY KEY (hotel_id)
);

ALTER TABLE hoteles AUTO_INCREMENT = 30000;

USE hospedajes;

INSERT INTO hoteles (nombre, barrio, direccion, descripcion, servicios, telefono, email)
VALUES ("Hotel Paz", "Recoleta", "Ayacucho 1849", "Un hotel muy tranquilo para despejar los malos aires de la capital", "WI-FI, desayuno, pileta, paseo en barco", "5411435665", "laPazContacto@lapazhotel.com"),
('Hotel Alvear', 'La Recoleta', 'Av. Alvear 1891', 'Hotel de lujo en el corazón de Buenos Aires.', 'Spa, piscina, restaurante gourmet', '+54 11 4808-9100', 'info@alvear.com.ar'),
('Sheraton Buenos Aires', 'Retiro', 'Av. del Libertador 440', 'Hotel elegante con vistas al Río de la Plata.', 'Gimnasio, piscina cubierta, bar', '+54 11 4318-9000', 'reservas@sheraton.com'),
('Hotel Panamericano', 'Microcentro', 'Av. Carlos Pellegrini 551', 'Ubicado cerca de los principales puntos turísticos.', 'Restaurante, sala de conferencias, Wi-Fi gratuito', '+54 11 5279-0000', 'info@panamericano.com.ar'),
('Faena Hotel Buenos Aires', 'Puerto Madero', 'Martha Salotti 445', 'Hotel boutique con un diseño único y exclusivo.', 'Spa, piscina al aire libre, bar de cócteles', '+54 11 4010-9200', 'reservas@faena.com'),
('Hotel NH Buenos Aires City', 'Monserrat', 'Cerrito 154', 'Moderno hotel con fácil acceso al transporte público.', 'Desayuno buffet, gimnasio, servicio de habitaciones', '+54 11 4314-6000', 'nhcity@nh-hotels.com'),
("Hotel La Estación", "Caballito", "Rivadavia 4500", "Ubicado en el corazón de Caballito, ideal para viajeros de negocios y turistas", "WI-FI, desayuno, gimnasio, estacionamiento", "5411432123", "info@laestacionhotel.com"),
("Hotel Los Pinos", "La Matanza", "Avenida Juan Domingo Perón 2345", "Un hotel familiar y económico en la zona sur, perfecto para quienes buscan comodidad y buen precio", "Desayuno continental, WI-FI, parque, estacionamiento gratuito", "5411487654", "reservas@lospinoshotel.com"),
("Hotel Urban Suites", "Villa Urquiza", "Triunvirato 5500", "Moderno hotel boutique en Villa Urquiza, con diseño contemporáneo y atención personalizada", "WI-FI, pileta, desayuno buffet, room service", "5411456789", "contacto@urbansuiteshotel.com");
