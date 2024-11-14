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
            'id': row[0], 
            'reserva_id':row[1],
            'usuario_id': row[2],
            'hotel_id': row[3], 
            'habitacion_id':row[4],
            'fecha_entrada': row[5], 
            'fecha_salida': row[6]
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
    return jsonify({'id': result[0], 'reserva_id': result[1]}), 200

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
            'imagen_principal': row[1], 
            'barrio': row[2],
            'nombre': row[3],
            'descripcion': row[4],
            'direccion': row[5]
        })

    return jsonify(response), 200

@app.route('/api/hoteles/<int:hotel_id>', methods=['GET'])
def obtener_hotel_by_id(hotel_id):
    fecha_entrada = request.args.get('fecha_entrada')
    fecha_salida = request.args.get('fecha_salida')
    cantidad_personas = request.args.get('cantidad_personas')

    try:
        result_hotel = querys.obtener_hotel_by_id(hotel_id)
        result_habitaciones = querys.obtener_todas_las_habitaciones_del_hotel(hotel_id, fecha_entrada, fecha_salida, cantidad_personas)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    
    if not result_hotel:
        return jsonify({'error': 'No se ha encontrado un hotel con el ID dado'})
    
    if not result_habitaciones:
        return jsonify({'error': 'No se ha encontrado una habitación para el hotel dado'})
    
    response_hotel = {
        'nombre': result_hotel[0],
        'barrio': result_hotel[1],
        'direccion': result_hotel[2],
        'descripcion': result_hotel[3],
        'servicios': result_hotel[4],
        'telefono': result_hotel[5],
        'email': result_hotel[6],
        'imagen_principal': result_hotel[7],
        'puntuacion': result_hotel[8]
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
        result = querys.obtener_habitacion_by_id(habitacion_id)
    except Exception as e:
        return jsonify({ 'error': str(e) }), 404
    
    if result is None:
        return jsonify({ 'error': 'No se ha encontrado una habitacion con el ID dado' }), 404
    
    response = {
        'habitacion_id' : result[0],
        'hotel_id' : result[1],
        'nombre' : result[2],
        'descripcion' : result[3],
        'precio' : result[4],
        'capacidad' : result[5]
    }

    return jsonify(response), 200

    
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




if __name__ == "__main__":
    app.run("127.0.0.1", port = PORT, debug = True)
