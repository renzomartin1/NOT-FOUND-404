from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
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

@app.route('/api/reservas', methods = ['POST'])
def crear_reservas():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    usuario_id = data.get('usuario_id')
    hotel_id = data.get('hotel_id')
    habitacion_id = data.get('habitacion_id')
    fecha_entrada = data.get('fecha_inicio')
    fecha_salida = data.get('fecha_fin')
    querys.registrar_reserva({'usuario_id':usuario_id, 'hotel_id':hotel_id, 'habitacion_id':habitacion_id, 'fecha_entrada':fecha_entrada, 'fecha_salida':fecha_salida})

    return jsonify(), 201

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
        print(result)
    
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
    print (response_habitaciones)

    return jsonify({'hotel': response_hotel, 'habitaciones': response_habitaciones}), 200


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
            'telefono': row[3]
        })
    return jsonify(response), 200


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
    query_verificacion = "SELECT email, numero FROM usuarios WHERE email = :email OR numero = :numero;"

    try:
        resultado_query_verificacion = querys.run_query(query_verificacion, datos_register)
    except SQLAlchemyError as error:
        return jsonify({"error": str(error)}), 500

    if resultado_query_verificacion.rowcount == 0:
        query_register = "INSERT INTO usuarios (nombre, apellido, email, contraseña, numero) VALUES (:nombre, :apellido, :email, :contraseña, :numero);"

        try:
            querys.run_query(query_register, datos_register)
        except SQLAlchemyError as error:
            return jsonify({"error": str(error)}), 500

        return jsonify({"success": "Usuario registrado correctamente."}), 201

    elif resultado_query_verificacion.rowcount == 1:
        fila = resultado_query_verificacion.fetchone()

        if datos_register["email"] == fila.email and datos_register["numero"] == fila.numero:
            return jsonify({"error": "El correo electrónico o el número telefónico ya se encuentran registrados."}), 400

        elif datos_register["email"] == fila.email:
            return jsonify({"error": "El correo electrónico o el número telefónico ya se encuentran registrados."}), 400

        elif datos_register["numero"] == fila.numero:
            return jsonify({"error": "El correo electrónico o el número telefónico ya se encuentran registrados."}), 400

    elif resultado_query_verificacion.rowcount == 2:
        return jsonify({"error": "El correo electrónico o el número telefónico ya se encuentran registrados."}), 400


@app.route("/api/usuarios/login", methods = ["POST"])
def usuarios_login():
    datos_login = request.get_json()
    query_verificacion = "SELECT contraseña FROM usuarios WHERE email = :email;"

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
        return jsonify({"success": "Has iniciado sesión correctamente."}), 200
    

if __name__ == "__main__":
    app.run("127.0.0.1", port = PORT, debug = True)
