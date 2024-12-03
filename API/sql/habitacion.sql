-- (para evitar errores si se vuelve a ejecutar el script (eliminar luego))
DROP TABLE IF EXISTS habitaciones;

-- Crear la tabla habitaciones
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


INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30000, "Habitación Tranquilidad", "Habitación amplia con vista al jardín interior, ideal para descansar y desconectar del ruido urbano", 100, 3, 5),
(30000, "Suite Serenidad", "Suite de lujo con balcón privado y vista panorámica de la ciudad, perfecta para una estancia relajante", 135, 2, 4),
(30000, "Habitación Zen", "Hab. sencilla pero acogedora, con decoración minimalista y una atmósfera tranquila para descansar profundamente", 80, 1, 3),
(30000, "Suite Relax", "Suite espaciosa con jacuzzi privado y un balcon espacioso, para una experiencia de total relajación", 150, 4, 2),
(30000, "Habitación familiar", "Ideal para disfrutar con la familia de una jornada de descanso, rodeado de silencio y paz", 170, 5, 1);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30001, "Suite Real", "Exclusiva suite con vista a la Avenida Alvear, equipada con jacuzzi y mobiliario de lujo", 500, 2, 3),
(30001, "Habitación Premier", "Habitación de lujo con decoración clásica, baño de mármol y acceso a la piscina", 350, 2, 4),
(30001, "Suite Ejecutiva", "Perfecta para viajeros de negocios, con escritorio, acceso a Wi-Fi de alta velocidad y salón privado", 400, 1, 2),
(30001, "Habitación Alvear", "Habitación elegante con una cama king-size, ideal para una estadía relajante", 280, 2, 5),
(30001, "Suite Presidencial", "Una de las suites más exclusivas del hotel, con salón privado y vistas panorámicas", 800, 3, 1);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30002, "Habitación Vista Río", "Habitación elegante con vistas al Río de la Plata, perfecta para una estancia tranquila", 300, 2, 5),
(30002, "Suite Executive", "Suite de lujo con salón privado y acceso a todos los servicios del club ejecutivo", 500, 3, 5),
(30002, "Habitación Superior", "Habitación moderna con amplio baño y vistas impresionantes al puerto", 250, 2, 4),
(30002, "Suite del Libertador", "Suite espaciosa con área de estar, ideal para huéspedes que buscan comodidad y estilo", 450, 2, 3),
(30002, "Habitación Club", "Habitación con acceso al Club Lounge, ideal para viajeros frecuentes", 350, 2, 3);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30003, "Habitación Ejecutiva", "Habitación moderna con escritorio, ideal para viajeros de negocios", 100, 1, 2),
(30003, "Suite Panamericana", "Suite amplia con vistas al Obelisco y acceso a los principales puntos turísticos", 400, 3, 3),
(30003, "Habitación Standard", "Habitación cómoda con todas las comodidades para un descanso reparador", 200, 5, 5),
(30003, "Habitación Premium", "Habitación con detalles de lujo, ideal para aquellos que buscan más confort", 280, 4, 5),
(30003, "Suite Premium", "Suite de lujo con baño de mármol, sala de estar y vista al centro de Buenos Aires", 500, 2, 5);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30004, "Suite Faena", "Habitación de lujo con diseño único, bañera de hidromasaje y acceso al spa, acceso a barra libre", 600, 2, 3),
(30004, "Habitación Marina", "Habitación elegante con vista al puerto y decoración exclusiva de alto diseño", 230, 1, 3),
(30004, "Suite Arte", "Suite decorada con arte contemporáneo, ideal para los amantes de la cultura y el diseño", 500, 3, 3),
(30004, "Habitación Deluxe", "Habitación amplia con cama king-size, ideal para una estancia tranquila y cómoda", 400, 2, 3),
(30004, "Suite Penthouse", "La suite más exclusiva del hotel, con piscina privada y vistas espectaculares de Puerto Madero", 1000, 4, 3);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30005, "Habitación Confort", "Habitación moderna con cama doble y vistas a la ciudad", 180, 2, 2),
(30005, "Suite NH", "Suite espaciosa con área de estar, baño de lujo y Wi-Fi de alta velocidad", 350, 3, 1),
(30005, "Habitación Business", "Habitación adaptada para viajeros de negocios, con escritorio y servicios especiales", 220, 2, 5),
(30005, "Habitación Superior", "Habitación moderna con cama queen-size, ideal para descansar después de un día de trabajo", 250, 2, 5),
(30005, "Suite Ejecutiva", "Suite de lujo con vista a la ciudad, escritorio ejecutivo y acceso a la zona VIP", 400, 3, 2);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30006, "Habitación Estación", "Habitación cómoda y tranquila con vista al parque, perfecta para descansar", 120, 2, 1),
(30006, "Suite Ejecutiva", "Ideal para ejecutivos, con escritorio, Wi-Fi de alta velocidad y acceso a la zona de negocios", 220, 2, 1),
(30006, "Habitación Familiar", "Amplia habitación para familias con dos camas dobles y vista a la ciudad", 180, 4, 1),
(30006, "Habitación Sencilla", "Habitación sencilla pero acogedora, ideal para una estadia corta", 80, 1, 1),
(30006, "Suite Premium", "Suite con decoración moderna, cama king-size y área de trabajo", 250, 2, 1);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30007, "Habitación Estándar", "Habitación cómoda y accesible, ideal para una estancia económica en familia", 100, 2, 3),
(30007, "Habitación Doble", "Habitación con dos camas individuales, ideal para compartir", 120, 2, 3),
(30007, "Suite Familiar", "Amplia suite con dos habitaciones y servicios completos para la familia", 250, 5, 3),
(30007, "Habitación Deluxe", "Habitación con cama king-size y acceso a todos los servicios del hotel", 160, 1, 2),
(30007, "Habitación Triple", "Ideal para grupos o familias pequeñas, con tres camas y baño privado", 180, 3, 5);

INSERT INTO habitaciones (hotel_id, nombre, descripcion, precio, capacidad, calificacion)
VALUES 
(30008, "Habitación Deluxe", "Habitación moderna con cama queen-size, ideal para descansar después de un día de trabajo", 150, 2, 4),
(30008, "Suite Urban", "Suite con diseño contemporáneo, ideal para una experiencia más lujosa en Villa Urquiza", 300, 2, 4),
(30008, "Habitación Confort", "Habitación simple con decoración minimalista, perfecta para una estancia corta", 120, 2, 4),
(30008, "Suite Panorama", "Suite con ventanales grandes y vistas a la ciudad, equipada con todos los servicios de lujo", 350, 3, 2),
(30008, "Habitación Familiar", "Habitación con dos camas dobles, ideal para familias o pequeños grupos", 200, 4, 1);
