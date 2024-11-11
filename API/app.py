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


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)