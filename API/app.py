from flask import Flask, jsonify, request
import querys


app = Flask(__name__)
PORT = 5000


#-------------------------------- inicio reservaciones ------------------------------------------------
@app.route('/api/reservas', methods = ['GET'])
def get_all_reservas():
    try:
        result = querys.all_reservas()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({ 
            'reserva_id':row[0],
            'usuario_id': row[1],
            'hotel_id': row[2], 
            'habitacion_id':row[3],
            'fecha_entrada': row[4], 
            'fecha_salida': row[5]
        })

    return jsonify(response), 200

@app.route('/api/reservas/<int:usuario_id>', methods=['GET'])
def reserva_by_usuario_id(usuario_id):
    try:
        result = querys.reserva_by_usuario_id(usuario_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if len(result) == 0:
        return jsonify({'error': 'No se encontró la reserva'}), 404 # Not found

    result = result[0]
    return jsonify({'reserva_id': result[0]}), 200

#------------------------------------------- fin reservaciones--------------------------------------------


@app.route('/api/hoteles', methods=['GET'])
def filtrar_hoteles():
    
    fecha_entrada = request.args.get('fecha_entrada')
    fecha_salida = request.args.get('fecha_salida')
    cantidad_personas = request.args.get('cantidad_personas')
    
    if cantidad_personas:
        cantidad_personas = int(cantidad_personas)
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
            'direccion': row[4],
            'descripcion': row[5]
        })

    return jsonify(response), 200

@app.route('/api/hoteles/<int:hotel_id>', methods=['GET'])
def obtener_hotel_by_id(hotel_id):
    fecha_entrada = request.args.get('fecha_entrada')
    fecha_salida = request.args.get('fecha_salida')
    cantidad_personas = request.args.get('cantidad_personas')

    try:
        result_hotel = querys.obtener_hotel_by_id(hotel_id)
        result_habitaciones = querys.filtrar_habitaciones(hotel_id, fecha_entrada, fecha_salida, cantidad_personas)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    
    if not result_hotel:
        return jsonify({'error': 'No se ha encontrado un hotel con el ID dado'})
    
    if not result_habitaciones:
        return jsonify({'error': 'No se ha encontrado una habitación para el hotel dado'})
    
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




@app.route('/api/habitacion/<int:habitacion_id>', methods = ['GET'])
def habitacion_by_id(habitacion_id):   
    try:
        result_habitacion = querys.obtener_habitacion_by_id(habitacion_id)
        result_otras_habitaciones = querys.filtrar_habitaciones(hotel_id=result_habitacion[1], habitacion_id=habitacion_id, fecha_entrada=None, fecha_salida=None, cantidad_personas=None)
    except Exception as e:
        return jsonify({ 'error': str(e) }), 404
    
    if result_habitacion is None or result_otras_habitaciones is None:
        return jsonify({ 'error': 'No se ha encontrado una habitacion con el ID dado' }), 404
    
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

    return jsonify({'habitacion': response_habitacion, 'otras_habitaciones': response_otras_habitaciones}), 200

    
@app.route('/api/usuarios', methods = ['GET'])
def obtener_todos_los_usuarios():
    try:
        result = querys.obtener_todos_los_usuarios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    response = []
    for row in result:
        response.append({
            'nombre': row[0],
            'apellido': row[1],
            'email': row[2],
            'numero': row[3]
        })
    return jsonify(response), 200

@app.route('/api/usuarios/<int:usuario_id>', methods = ['GET'])
def obtener_usuario_por_id(usuario_id):
    try:
        result = querys.obtener_usuario_by_id(usuario_id)
    except Exception as e:
        return jsonify({ 'error': str(e) }), 404
    
    if result is None:
        return jsonify({ 'error': 'No se ha encontrado un usuario con el ID dado' })
    
    response = {
        'nombre': result[0],
        'apellido': result[1],
        'email': result[2],
        'numero': result[3]
    }
    return jsonify(response), 200

@app.route('/api/usuarios/<int:usuario_id>', methods = ['DELETE'])
def eliminar_usuario_por_id(usuario_id):
    usuario_data = querys.obtener_usuario_by_id(usuario_id)
    if not usuario_data:
        return jsonify({'error': 'No se ha encontrado un usuario con el ID dado'}), 404

    # Eliminar usuario
    querys.eliminar_usuario(usuario_id)
    response = {
        'nombre': usuario_data[0],
        'apellido': usuario_data[1],
        'email': usuario_data[2],
        'numero': usuario_data[3]
    }
    return jsonify(response), 200


@app.route("/api/usuarios/register", methods = ["POST"])
def usuarios_register():
    register = request.get_json()
    query_verificacion = f"SELECT email, numero FROM usuarios WHERE email = '{register["email"]}' OR numero = {register["numero"]};"

    try:
        resultado_query_verificacion = querys.run_query(query_verificacion)
    except SQLAlchemyError as error:
        return jsonify({"error": str(error)}), 500

    if resultado_query_verificacion.rowcount == 0:
        query_register = f"INSERT INTO usuarios (nombre, apellido, email, contraseña, numero) VALUES ('{register["nombre"]}', '{register["apellido"]}', '{register["email"]}', '{register["contraseña"]}', {register["numero"]});"

        try:
            querys.run_query(query_register)
        except SQLAlchemyError as error:
            return jsonify({"error": str(error)}), 500

        return jsonify({"success": "Usuario registrado exitosamente."}), 201

    elif resultado_query_verificacion.rowcount == 1:
        fila = resultado_query_verificacion.fetchone()

        if register["email"] == fila.email and register["numero"] == fila.numero:
            return jsonify({"error": "E-mail y número no disponibles (v1)."}), 400

        elif register["email"] == fila.email:
            return jsonify({"error": "E-mail no disponible."}), 400

        elif register["numero"] == fila.numero:
            return jsonify({"error": "Número no disponible."}), 400

    elif resultado_query_verificacion.rowcount == 2:
        return jsonify({"error": "E-mail y número no disponibles (v2)."}), 400


@app.route("/api/usuarios/login", methods = ["POST"])
def usuarios_login():
    login = request.get_json()
    query_verificacion = f"SELECT contraseña FROM usuarios WHERE email = '{login["email"]}';"

    try:
        resultado_query_verificacion = querys.run_query(query_verificacion)
    except SQLAlchemyError as error:
        return jsonify({"error": str(error)}), 500

    fila = resultado_query_verificacion.fetchone()

    if fila == None:
        return jsonify({"error": "El usuario no existe."}), 404

    elif login["contraseña"] != fila.contraseña:
        return jsonify({"error": "Contraseña incorrecta."}), 400

    else:
        return jsonify({"success": "Inicio de sesión exitoso."}), 200


if __name__ == "__main__":
    app.run("127.0.0.1", port = PORT, debug = True)