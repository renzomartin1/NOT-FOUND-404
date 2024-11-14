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
    try:
        fecha_entrada = request.args.get('fecha_entrada')
        fecha_salida = request.args.get('fecha_salida')
        cantidad_personas = request.args.get('cantidad_personas')

        if cantidad_personas:
            cantidad_personas = int(cantidad_personas)
        else:
            cantidad_personas = None  

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
    try:
        usuario_response = obtener_usuario_por_id(usuario_id)
        if len(usuario_response) == 0:
            return jsonify({ 'error': 'No se ha encontrado un usuario con el ID dado' })
        
        querys.eliminar_usuario(usuario_id)

    except Exception as e:
        return jsonify({ 'error': str(e) }), 500
    
    return usuario_response

if __name__ == "__main__":
    app.run("127.0.0.1", port = PORT, debug = True)
