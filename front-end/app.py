from flask import Flask, render_template, jsonify, request
from datetime import datetime
import requests

PORT = 5001
app = Flask(__name__)

API_URL = 'http://127.0.0.1:5000/api'

@app.route("/")
def home():
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")
    cantidad_personas = request.args.get("cantidad_personas")

    if not fecha_entrada:
        fecha_entrada = None
    if not fecha_salida:
        fecha_salida = None
    if not cantidad_personas:
        cantidad_personas = None
    
    try:
        params = {
            'fecha_entrada': fecha_entrada, 
            'fecha_salida': fecha_salida, 
            'cantidad_personas': cantidad_personas
        }
        response = requests.get(f"{API_URL}/hoteles", params=params)
        response.raise_for_status()
        hoteles = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500
        
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return render_template("home.html", hoteles=hoteles, fecha_actual=fecha_actual, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, cantidad_personas=cantidad_personas)


@app.route("/hotel/<int:hotel_id>")
def hotel(hotel_id, fecha_entrada=None, fecha_salida=None, cantidad_personas=None): 
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")
    cantidad_personas = request.args.get("cantidad_personas")

    if not fecha_entrada:
        fecha_entrada = None
    if not fecha_salida:
        fecha_salida = None
    if not cantidad_personas:
        cantidad_personas = None
    
    try:
        params = {
            'fecha_entrada': fecha_entrada, 
            'fecha_salida': fecha_salida, 
            'cantidad_personas': cantidad_personas
        }
        response = requests.get(f"{API_URL}/hoteles/{hotel_id}", params=params)
        response.raise_for_status()
        result = response.json()
        hotel = result["hotel"]
        habitaciones = result["habitaciones"]
    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return render_template("hotel.html", hotel=hotel, habitaciones=habitaciones, fecha_actual=fecha_actual)


@app.route("/habitacion/<int:habitacion_id>")
def habitacion(habitacion_id):
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")

    try:
        response = requests.get(f"{API_URL}/habitacion/{habitacion_id}")
        response.raise_for_status()
        habitacion = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500
    
    return render_template("habitacion.html", habitacion=habitacion, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida)


@app.route("/confirmacion-compra")
def comprar():
    return render_template("confirmacion_compra.html")


@app.errorhandler(404)      #manejo de errores
def error_404(e):
    return render_template('404.html'), 404


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


@app.route("/sobre-nosotros")
def sobre_nosotros():
    return render_template("sobre_nosotros.html")


if __name__ == "__main__":
    app.run(debug = True, port = PORT)