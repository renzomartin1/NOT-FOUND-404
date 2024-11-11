from flask import Flask, jsonify, request

import querys

app = Flask(__name__)

@app.route('/api/reservas', methods=['GET'])
def get_all_reservas():
    try:
        result = querys.all_reservas()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'id':row[0], 'id_reserva': row[1], 'id_habitacion':row[3], 'fecha_entrada':row[4], 'fecha_salida': row[5]})

    return jsonify(response), 200


@app.route('/api/hoteles', methods=['GET'])
def filtrar_hoteles():
    try:
        ubicacion = request.args.get('ubicacion')
        cantidad_personas = request.args.get('cantidad_personas')

        if cantidad_personas:
            cantidad_personas = int(cantidad_personas)
        else:
            cantidad_personas = None  

        result = querys.filtrar_hoteles(ubicacion, cantidad_personas)
    
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


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)