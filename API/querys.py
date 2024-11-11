from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

QUERY_TODAS_LAS_RESERVAS = "SELECT id, id_reserva, id_habitacion, fecha_entrada, fecha_salida FROM reservas"

# string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
#engine = create_engine("mysql://root:root@localhost:3308/IDS_API")
engine = create_engine("mysql+mysqlconnector://renzo:123@localhost:3306/hospedajes")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

def all_reservas():
    return run_query(QUERY_TODAS_LAS_RESERVAS).fetchall()