from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Usuarios
QUERY_OBTENER_TODOS_LOS_USUARIOS = "SELECT nombre, apellido, email, numero FROM usuarios"
QUERY_OBTENER_USUARIO_POR_ID = "SELECT nombre, apellido, email, numero FROM usuarios WHERE usuario_id = :usuario_id"
QUERY_ELIMINAR_USUARIO = "DELETE FROM usuarios WHERE usuario_id = :usuario_id"

# Reservas
QUERY_TODAS_LAS_RESERVAS = "SELECT id, reserva_id, usuario_id, hotel_id, habitacion_id, fecha_entrada, fecha_salida FROM reservaciones"
QUERY_RESERVA_BY_USUARIO_ID = "SELECT id, reserva_id FROM reservaciones WHERE usuario_id = :usuario_id"


# Hoteles
QUERY_OBTENER_TODOS_LOS_HOTELES = "SELECT nombre, barrio, direccion, descripcion, servicios, telefono, email, imagen_principal, puntuacion FROM hoteles"
QUERY_OBTENER_HOTELES_POR_ID = "SELECT nombre, barrio, direccion, descripcion, servicios, telefono, email, imagen_principal, puntuacion FROM hotele_id = :hotel_id"

QUERY_FILTRAR_HOTELES = """
SELECT h.hotel_id, h.imagen_principal, h.barrio, h.nombre, h.descripcion, h.direccion FROM hoteles h
INNER JOIN habitaciones hab ON h.hotel_id = hab.hotel_id
LEFT JOIN reservas res ON res.id_habitacion = hab.habitacion_id                        --El LEFT JOIN es para agarrar las habtiaciones que tienen reservas(para chequear si las fechas se solapan) como los que no
WHERE (                                                                                --con el INNER JOIN me traeria solo las habitaciones que esten la tabla habitaciones y reservas
    res.habitacion_id IS NULL OR  
   NOT (res.fecha_entrada < :fecha_salida AND res.fecha_salida > :fecha_entrada)
)
AND (:cantidad_personas IS NULL OR hab.cantidad_personas = :cantidad_personas)
GROUP BY h.hotel_id;
"""


# string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
# engine = create_engine("mysql://root:root@localhost:3308/IDS_API")
engine = create_engine("mysql+mysqlconnector://root:algo2@localhost:3306/hospedajes")

def run_query(query, parameters = None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

def obtener_todos_los_usuarios():
    return run_query(QUERY_OBTENER_TODOS_LOS_USUARIOS).fetchall()

def obtener_usuario_by_id(usuario_id):
    return run_query(QUERY_OBTENER_USUARIO_POR_ID, { 'usuario_id': usuario_id }).fetchone()

def eliminar_usuario(usuario_id):
    return run_query(QUERY_ELIMINAR_USUARIO, { 'usuario_id': usuario_id })
#-----------------------Reservas-------------------------------------------------------------------
def all_reservas():
    return run_query(QUERY_TODAS_LAS_RESERVAS).fetchall()

def reserva_by_usuario_id(usuario_id):
    return run_query(QUERY_RESERVA_BY_USUARIO_ID, {'usuario_id': usuario_id}).fetchall()
#------------------------Fin Reservas-------------------------------------------------------------------

def filtrar_hoteles(fecha_entrada, fecha_salida, cantidad_personas):
    return run_query(QUERY_FILTRAR_HOTELES, {"fecha_entrada":fecha_entrada, "fecha_salida":fecha_salida, "cantidad_personas":cantidad_personas}).fetchall()

def filtrar_hoteles(fecha_entrada, fecha_salida, cantidad_personas):#ademasa obtiene todos los hoteles
    return run_query(QUERY_FILTRAR_HOTELES, {"fecha_entrada":fecha_entrada, "fecha_salida":fecha_salida, "cantidad_personas":cantidad_personas}).fetchall()
    
def obtener_hotel_by_id(hotel_id):
    return run_query(QUERY_OBTENER_HOTEL_POR_ID, { 'hotel_id': hotel_id }).fetchone()
