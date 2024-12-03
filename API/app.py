from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
import querys


app = Flask(__name__)
PORT = 5005

#------------------------------------------- inicio reservaciones --------------------------------------------

@app.route('/api/reservas', methods = ['POST'])
def crear_reservas():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if not data:
        return jsonify({'error': 'no se ha proporcionado ninguna informacion'}), 400

    try:
        querys.registrar_reserva(data)
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(data), 201

@app.route('/api/reservas/<int:usuario_id>', methods=['GET'])
def reserva_by_usuario_id(usuario_id):
    try:
        result = querys.reserva_by_usuario_id(usuario_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({
            'reserva_id': row[0],
            'hotel_id': row[2],
            'habitacion_id': row[3], 
            'fecha_entrada': row[4], 
            'fecha_salida': row[5],
            'servicios': row[6],
            'usuario_id': row[1]
        })
    return jsonify(response), 200

@app.route('/api/reservas/<int:reserva_id>', methods=['DELETE'])
def eliminar_reserva(reserva_id):
    try:
        reserva = querys.eliminar_reserva(reserva_id)
        if not reserva:
            return jsonify({'error': 'reserva no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    try:
        querys.eliminar_reserva(reserva_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'reserva eliminada'}), 200

@app.route('/api/reservas/<int:reserva_id>', methods=['GET'])
def reserva_by_reserva_id(reserva_id):
    try:
        result = querys.reserva_by_reserva_id(reserva_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if result is None:
        return jsonify({'error': 'No se ha encontrado una reserva con el ID dado'}), 404

    response = {
        'reserva_id': result[0],
        'hotel_id': result[1],
        'habitacion_id': result[2], 
        'fecha_entrada': result[3], 
        'fecha_salida': result[4]
    }
    return jsonify(response), 200

@app.route('/api/verificar_reserva', methods=['POST'])
def verificar_reserva():
    data = request.json
    reserva_id = data.get('reserva_id')
    usuario_id = data.get('usuario_id')
    try:
        result = querys.reserva_by_reserva_id_usuario_id(reserva_id, usuario_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if result:
        return jsonify({'message': 'reserva encontrada', "usuario_id": result[0], "reserva_id": result[1]}), 200
    else:
        return jsonify({'message': 'reserva no encontrada'}), 404
    
@app.route('/api/actualizar_servicios', methods=['PUT'])
def actualizar_servicios():
    data = request.get_json()
    servicios_contratados = data.get("servicios_contratados")
    reserva_id = data.get("reserva_id")

    if not servicios_contratados or not reserva_id:
        return jsonify({"error": "Faltan datos necesarios"}), 400

    try:
        querys.actualizar_servicios(reserva_id, servicios_contratados)
        return jsonify({"message": "Servicios contratados actualizados con éxito"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar los servicios: {str(e)}"}), 500

@app.route('/api/reservas_habitacion/<int:habitacion_id>', methods=['GET'])
def reservas_habitacion(habitacion_id):
    fecha_entrada = request.args.get('fecha_entrada')
    fecha_salida = request.args.get('fecha_salida')

    if not fecha_entrada or not fecha_salida:
        return jsonify({'error': 'Faltan parámetros: fecha_entrada o fecha_salida'}), 400

    try:
        result = querys.reservas_habitacion(habitacion_id, fecha_entrada, fecha_salida)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({
            'reserva_id': row[0],
            'hotel_id': row[1],
            'habitacion_id': row[2], 
            'fecha_entrada': row[3], 
            'fecha_salida': row[4]
        })
    return jsonify(response), 200
#------------------------------------------- fin reservaciones --------------------------------------------

#------------------------------------------- inicio hoteles -----------------------------------------------

@app.route('/api/hoteles', methods=['GET'])
def filtrar_hoteles():
    
    fecha_entrada = request.args.get('fecha_entrada')
    fecha_salida = request.args.get('fecha_salida')
    cantidad_personas = request.args.get('cantidad_personas')
    
    if cantidad_personas:
        try:
            cantidad_personas = int(cantidad_personas)
        except Exception:
            cantidad_personas = None
    else:
        cantidad_personas = None

    try:
        result = querys.filtrar_hoteles(fecha_entrada,fecha_salida, cantidad_personas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({
            'hotel_id': row[0],
            'nombre': row[1],
            'barrio': row[2],
            'direccion': row[3],
            'descripcion': row[4],
            'servicios': row[5]
        })

    return jsonify(response), 200

@app.route('/api/hoteles/<int:hotel_id>', methods=['GET'])
def obtener_hotel_by_id(hotel_id):  #hotel_by_id_y_habitaciones_hotel
    fecha_entrada = request.args.get('fecha_entrada')
    fecha_salida = request.args.get('fecha_salida')
    cantidad_personas = request.args.get('cantidad_personas')

    try:
        result_hotel = querys.obtener_hotel_by_id(hotel_id)
        result_habitaciones = querys.filtrar_habitaciones(hotel_id, None, fecha_entrada, fecha_salida, cantidad_personas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    if not result_hotel:
        return jsonify({'error': 'No se ha encontrado un hotel con el ID dado'}), 404
    
    if not result_habitaciones:
        return jsonify({'error': 'No se ha encontrado una habitación para el hotel dado'}), 404
    
    response_hotel = {
        'nombre': result_hotel[1],
        'barrio': result_hotel[2],
        'direccion': result_hotel[3],
        'descripcion': result_hotel[4],
        'servicios': result_hotel[5],
        'telefono': result_hotel[6],
        'email': result_hotel[7]
    }

    response_habitaciones = []
    for row in result_habitaciones:
        response_habitaciones.append({
            'habitacion_id': row[0],
            'hotel_id': row[1],
            'nombre': row[2],
            'descripcion': row[3],
            'precio': row[4],
            'capacidad': row[5]
        })

    return jsonify({'hotel': response_hotel, 'habitaciones': response_habitaciones}), 200


@app.route('/api/hoteles/servicios/<int:hotel_id>', methods=['GET'])
def obtener_servicios_por_id(hotel_id):
    try:
        result = querys.obtener_hotel_by_id(hotel_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if result is None:
        return jsonify({'error': 'No se ha encontrado un hotel con el ID dado'}), 404

    return jsonify({'servicios': result[5]}), 200

#------------------------------------------- fin hoteles -------------------------------------------------------

#------------------------------------------- inicio habitaciones -----------------------------------------------

@app.route('/api/habitacion/<int:habitacion_id>', methods = ['GET'])
def habitacion_by_id(habitacion_id):   #habitacion_by_id_y_otras_habitaciones
    try:
        result_habitacion = querys.obtener_habitacion_by_id(habitacion_id)
        result_otras_habitaciones = querys.filtrar_habitaciones(hotel_id=result_habitacion[1], habitacion_id=habitacion_id, fecha_entrada=None, fecha_salida=None, cantidad_personas=None)
        result_hotel = querys.obtener_hotel_by_id(hotel_id=result_habitacion[1])
    except Exception as e:
        return jsonify({ 'error': str(e) }), 404
    
    if result_habitacion is None or result_otras_habitaciones is None:
        return jsonify({ 'error': 'No se ha encontrado una habitacion con el ID dado' }), 404
    
    response_hotel = {
        'hotel_id' : result_hotel[0],
        'hotel_nombre' : result_hotel[1]
    }

    response_habitacion = {
        'habitacion_id' : result_habitacion[0],
        'hotel_id' : result_habitacion[1],
        'nombre' : result_habitacion[2],
        'descripcion' : result_habitacion[3],
        'precio' : result_habitacion[4],
        'capacidad' : result_habitacion[5]
    }

    response_otras_habitaciones = []
    for row in result_otras_habitaciones:
        response_otras_habitaciones.append({
            'habitacion_id': row[0],
            'hotel_id': row[1],
            'nombre': row[2],
            'descripcion': row[3],
            'precio': row[4],
            'capacidad': row[5]
        })

    return jsonify({'habitacion': response_habitacion, 'otras_habitaciones': response_otras_habitaciones, 'hotel': response_hotel}), 200

#------------------------------------------- fin habitaciones -----------------------------------------------

#------------------------------------------- inicio usuarios ------------------------------------------------

@app.route('/api/usuarios/<int:usuario_id>', methods = ['GET'])
def obtener_usuario_por_id(usuario_id):
    try:
        result = querys.obtener_usuario_by_id(usuario_id)
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500
    
    if result is None:
        return jsonify({ 'error': 'No se ha encontrado un usuario con el ID dado' }), 404
    
    response = {
        'nombre': result[0],
        'apellido': result[1],
        'email': result[2],
        'telefono': result[3]
    }
    return jsonify(response), 200


@app.route('/api/usuarios/<int:usuario_id>', methods = ['DELETE'])
def eliminar_usuario_por_id(usuario_id):    
    try:
        usuario_data = querys.obtener_usuario_by_id(usuario_id)
        if not usuario_data:
            return jsonify({ 'error': 'No se ha encontrado un usuario con el ID dado' }), 404
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500
    
    try:
        querys.eliminar_usuario(usuario_id)
    except Exception as e:
        return jsonify({ 'error': 'Hubo un error en el servidor intentando eliminar el usuario' }), 500
    
    return jsonify({ 'message': 'El usuario ha sido eliminado con éxito' }), 200


@app.route("/api/usuarios/register", methods = ["POST"])
def usuarios_register():
    datos_register = request.get_json()
    query_verificacion = "SELECT email, telefono FROM usuarios WHERE email = :email OR telefono = :telefono;"

    try:
        resultado_query_verificacion = querys.run_query(query_verificacion, datos_register)
    except SQLAlchemyError as error:
        return jsonify({"error": str(error)}), 500

    if resultado_query_verificacion.rowcount == 0:
        query_register = "INSERT INTO usuarios (nombre, apellido, email, contraseña, telefono) VALUES (:nombre, :apellido, :email, :contraseña, :telefono);"

        try:
            querys.run_query(query_register, datos_register)
        except SQLAlchemyError as error:
            return jsonify({"error": str(error)}), 500

        return jsonify({"success": "Usuario registrado correctamente."}), 201

    elif resultado_query_verificacion.rowcount == 1:
        fila = resultado_query_verificacion.fetchone()

        if datos_register["email"] == fila.email and datos_register["telefono"] == fila.telefono:
            return jsonify({"error": "El correo electrónico y el número telefónico ya se encuentran registrados."}), 400

        elif datos_register["email"] == fila.email:
            return jsonify({"error": "El correo electrónico ya se encuentra registrado."}), 400

        elif datos_register["telefono"] == fila.telefono:
            return jsonify({"error": "El número telefónico ya se encuentra registrado."}), 400

    elif resultado_query_verificacion.rowcount == 2:
        return jsonify({"error": "El correo electrónico y el número telefónico ya se encuentran registrados."}), 400


@app.route("/api/usuarios/login", methods = ["POST"])
def usuarios_login():
    datos_login = request.get_json()
    query_verificacion = "SELECT usuario_id, contraseña FROM usuarios WHERE email = :email;"

    try:
        resultado_query_verificacion = querys.run_query(query_verificacion, datos_login)
    except SQLAlchemyError as error:
        return jsonify({"error": str(error)}), 500

    fila = resultado_query_verificacion.fetchone()

    if fila == None:
        return jsonify({"error": "No hay ningún usuario asociado a este correo electrónico."}), 404

    elif datos_login["contraseña"] != fila.contraseña:
        return jsonify({"error": "La contraseña es incorrecta."}), 400

    else:
        return jsonify({"usuario_id": fila.usuario_id}), 200
    

@app.route('/api/verificar_usuario', methods=['POST'])
def verificar_usuario():
    data = request.json
    email = data.get('email')
    contraseña = data.get('contraseña')

    result = querys.obtener_usuario_by_email(email, contraseña)
    print("Resultado de la consulta:", result)

    if result:
        return jsonify({"status": "success", "usuario_id": result[0]})
    else:
        return jsonify({"status": "error", "message": "Usuario o contraseña incorrectos"}), 401

#------------------------------------------- fin usuarios ------------------------------------------------

if __name__ == "__main__":
    app.run("127.0.0.1", port = PORT, debug = True)

