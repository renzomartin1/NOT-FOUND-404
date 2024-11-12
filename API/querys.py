from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Usuarios
QUERY_OBTENER_TODOS_LOS_USUARIOS = "SELECT nombre, apellido, email, numero FROM usuarios"
QUERY_OBTENER_USUARIO_POR_ID = "SELECT nombre, apellido, email, numero FROM usuarios WHERE usuario_id = :usuario_id"

# Reservas
QUERY_TODAS_LAS_RESERVAS = "SELECT id, id_reserva, id_habitacion, fecha_entrada, fecha_salida FROM reservas"

# Hoteles
QUERY_FILTRAR_HOTELES = """
SELECT h.hotel_id, h.imagen_principal, h.barrio, h.nombre, h.descripcion, h.direccion FROM hoteles h
INNER JOIN habitaciones hab ON h.hotel_id = hab.hotel_id
WHERE (h.ubicacion = :ubicacion OR :ubicacion IS NULL) AND hab.reservado = 0
AND (:cantidad_personas IS NULL OR hab.cantidad_personas = :cantidad_personas)
GROUP BY h.hotel_id;
"""


# string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
# engine = create_engine("mysql://root:root@localhost:3308/IDS_API")
engine = create_engine("mysql+mysqlconnector://renzo:123@localhost:3306/hospedajes")

def run_query(query, parameters = None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

def obtener_todos_los_usuarios():
    return run_query(QUERY_OBTENER_TODOS_LOS_USUARIOS).fetchall()

def obtener_usuario_by_id(usuario_id):
    return run_query(QUERY_OBTENER_USUARIO_POR_ID, { 'usuario_id': usuario_id }).fetchone()

def all_reservas():
    return run_query(QUERY_TODAS_LAS_RESERVAS).fetchall()

def filtrar_hoteles(ubicacion, cantidad_personas):
    return run_query(QUERY_FILTRAR_HOTELES, {"ubicacion":ubicacion, "cantidad_personas":cantidad_personas}).fetchall()