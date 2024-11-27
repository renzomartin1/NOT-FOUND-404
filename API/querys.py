from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os

# Usuarios
QUERY_OBTENER_TODOS_LOS_USUARIOS = "SELECT nombre, apellido, email, telefono FROM usuarios"
QUERY_OBTENER_USUARIO_POR_ID = "SELECT nombre, apellido, email, telefono FROM usuarios WHERE usuario_id = :usuario_id"
QUERY_ELIMINAR_USUARIO = "DELETE FROM usuarios WHERE usuario_id = :usuario_id"
QUERY_OBTENER_USUARIO_POR_EMAIL = "SELECT * FROM usuarios WHERE email = :email AND contraseña = :contraseña"

# Reservas
QUERY_TODAS_LAS_RESERVAS = "SELECT reserva_id, usuario_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida FROM reservaciones"
QUERY_RESERVA_BY_USUARIO_ID = "SELECT reserva_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida FROM reservaciones WHERE usuario_id = :usuario_id"
QUERY_REGISTRAR_RESERVA = """
INSERT INTO reservaciones(usuario_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida)
VALUES
(:usuario_id, :hotel_id, :habitacion_id, :fecha_entrada, :fecha_salida);
"""
QUERY_ELIMINAR_RESERVA = "DELETE FROM reservaciones WHERE reserva_id = :reserva_id"
QUERY_RESERVA_BY_RESERVAID_USUARIOID = "SELECT * FROM reservaciones WHERE usuario_id = :usuario_id AND reserva_id = :reserva_id"


# Hoteles
QUERY_OBTENER_TODOS_LOS_HOTELES = "SELECT * FROM hoteles"
QUERY_OBTENER_HOTELES_POR_ID = "SELECT * FROM hoteles WHERE hotel_id = :hotel_id"

QUERY_FILTRAR_HOTELES = """
SELECT h.hotel_id, h.nombre, h.barrio, h.direccion, h.descripcion, h.servicios FROM hoteles h
INNER JOIN habitaciones hab ON h.hotel_id = hab.hotel_id
LEFT JOIN reservaciones res ON res.habitacion_id = hab.habitacion_id                         
WHERE (                                                                                
    res.habitacion_id IS NULL OR  
    NOT (res.fecha_entrada < :fecha_salida AND res.fecha_salida > :fecha_entrada)
)
AND (:cantidad_personas IS NULL OR hab.capacidad = :cantidad_personas)
GROUP BY h.hotel_id, h.barrio, h.nombre, h.descripcion, h.direccion;
"""

#HABITACIONES
QUERY_FILTRAR_HABITACIONES = """
SELECT hab.habitacion_id, hab.hotel_id, hab.nombre, hab.descripcion, hab.precio, hab.capacidad 
FROM habitaciones hab
INNER JOIN hoteles ON :hotel_id = hab.hotel_id
LEFT JOIN reservaciones res ON res.habitacion_id = hab.habitacion_id
WHERE :hotel_id = :hotel_id 
AND (:habitacion_id IS NULL OR hab.habitacion_id != :habitacion_id)
AND (
    (:fecha_entrada IS NULL AND :fecha_salida IS NULL) OR
    res.habitacion_id IS NULL OR
    NOT (res.fecha_entrada < :fecha_salida AND res.fecha_salida > :fecha_entrada)
)
AND (:cantidad_personas IS NULL OR hab.capacidad >= :cantidad_personas)
GROUP BY hab.habitacion_id, hab.hotel_id, hab.nombre, hab.descripcion, hab.precio, hab.capacidad;
"""


QUERY_HABITACION_BY_ID = "SELECT hab.habitacion_id, hab.hotel_id, hab.nombre, hab.descripcion, hab.precio, hab.capacidad FROM habitaciones hab WHERE hab.habitacion_id = :habitacion_id"


# credenciales
db_username = os.getenv('MYSQL_USERNAME')
db_password = os.getenv('MYSQL_PASSWORD')

# string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
# engine = create_engine("mysql://'usuario':'contraseña'@localhost:'puerto'/'nombre_db'")
engine = create_engine(f"mysql+mysqlconnector://{db_username}:{db_password}:@localhost:3306/hospedajes")

def run_query(query, parameters = None):
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query), parameters)
            conn.commit()
            conn.close()
            return result
        except SQLAlchemyError as e:
            conn.rollback()
            raise e

def obtener_todos_los_usuarios():
    return run_query(QUERY_OBTENER_TODOS_LOS_USUARIOS).fetchall()

def obtener_usuario_by_id(usuario_id):
    return run_query(QUERY_OBTENER_USUARIO_POR_ID, { 'usuario_id': usuario_id }).fetchone()

def eliminar_usuario(usuario_id):
    return run_query(QUERY_ELIMINAR_USUARIO, { 'usuario_id': usuario_id })

def obtener_usuario_by_email(email, contraseña):
    return run_query(QUERY_OBTENER_USUARIO_POR_EMAIL, { 'email': email, 'contraseña': contraseña }).fetchone()

#-----------------------Reservas-------------------------------------------------------------------
def all_reservas():
    return run_query(QUERY_TODAS_LAS_RESERVAS).fetchall()

def registrar_reserva(data):
    return run_query(QUERY_REGISTRAR_RESERVA, data)

def reserva_by_usuario_id(usuario_id):
    return run_query(QUERY_RESERVA_BY_USUARIO_ID, {'usuario_id': usuario_id}).fetchall()

def eliminar_reserva(reserva_id):
    return run_query(QUERY_ELIMINAR_RESERVA, { 'reserva_id': reserva_id })

def reserva_by_reserva_id_usuario_id(reserva_id, usuario_id):
    return run_query(QUERY_RESERVA_BY_RESERVAID_USUARIOID, {'reserva_id': reserva_id, 'usuario_id': usuario_id}).fetchone()
#------------------------Fin Reservas-------------------------------------------------------------------

def filtrar_hoteles(fecha_entrada, fecha_salida, cantidad_personas):
    return run_query(QUERY_FILTRAR_HOTELES, {"fecha_entrada":fecha_entrada, "fecha_salida":fecha_salida, "cantidad_personas":cantidad_personas}).fetchall()

def obtener_hotel_by_id(hotel_id):
    return run_query(QUERY_OBTENER_HOTELES_POR_ID, { 'hotel_id': hotel_id }).fetchone()

def obtener_todos_los_hoteles(): 
    return run_query(QUERY_OBTENER_TODOS_LOS_HOTELES).fetchall()

#------------------------Habitaciones-------------------------------------------------------------------
def filtrar_habitaciones(hotel_id, habitacion_id, fecha_entrada, fecha_salida, cantidad_personas):
    return run_query(QUERY_FILTRAR_HABITACIONES, {"hotel_id":hotel_id, "habitacion_id":habitacion_id, "fecha_entrada":fecha_entrada, "fecha_salida":fecha_salida, "cantidad_personas":cantidad_personas}).fetchall()

def obtener_habitacion_by_id(habitacion_id):
    return run_query(QUERY_HABITACION_BY_ID, { 'habitacion_id': habitacion_id }).fetchone()

