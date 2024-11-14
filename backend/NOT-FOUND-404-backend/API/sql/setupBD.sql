-- Orquestador de la base de datos

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS hospedajes;
USE hospedajes;

-- Incluir archivos de tablas
SOURCE usuarios.sql;
SOURCE hoteles.sql;
SOURCE habitaciones.sql;
SOURCE reservas.sql;
