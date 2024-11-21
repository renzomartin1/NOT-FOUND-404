from flask import Flask, render_template, jsonify, request
from datetime import datetime
import requests

PORT = 5001
app = Flask(__name__)

API_URL = 'http://127.0.0.1:5005/api'

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
        response = requests.get(API_URL + '/habitacion/' + str(habitacion_id))
        response.raise_for_status()
        result = response.json()
        habitacion = result['habitacion']
        hotel = result['hotel']
        otras_habitaciones = result['otras_habitaciones']
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    return render_template("habitacion.html", habitacion=habitacion, otras_habitaciones=otras_habitaciones, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, hotel=hotel)


@app.route("/confirmacion_compra/<int:habitacion_id>")
def comprar(habitacion_id):
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")

    try:
        response = requests.get(API_URL + '/habitacion/' + str(habitacion_id))
        response.raise_for_status()
        result = response.json()
        habitacion = result['habitacion']
        hotel = result['hotel']
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    return render_template("confirmacion_compra.html", habitacion=habitacion, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, hotel=hotel)



@app.route("/perfil/<int:usuario_id>")
def perfil(usuario_id):
    dias_ES = {
        'Sunday': 'Domingo',
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado'
    }

    meses_ES = {
        'January': 'Enero',
        'February': 'Febrero',
        'March': 'Marzo',
        'April': 'Abril',
        'May': 'Mayo',
        'June': 'Junio',
        'July': 'Julio',
        'August': 'Agosto',
        'September': 'Septiembre',
        'October': 'Octubre',
        'November': 'Noviembre',
        'December': 'Diciembre'
    }
    try:
        usuario_response = requests.get(f"{API_URL}/usuarios/{usuario_id}")
        reservas_response = requests.get(f"{API_URL}/reservas/{usuario_id}")

        usuario_response.raise_for_status()
        reservas_response.raise_for_status()

        usuario_datos = usuario_response.json()
        reservas_datos = reservas_response.json()

        reservas_historial = []
        for reserva in reservas_datos:
            hotel_id = reserva['hotel_id']
            habitacion_id = reserva['habitacion_id']

            habitacion_response = requests.get(f"{API_URL}/habitacion/{habitacion_id}")
            habitacion_response.raise_for_status()
            habitacion_datos = habitacion_response.json()['habitacion']

            hotel_response = requests.get(f"{API_URL}/hoteles/{hotel_id}")
            hotel_response.raise_for_status()
            hotel_datos = hotel_response.json()['hotel']

            fecha_entrada = str(reserva['fecha_entrada'])
            fecha_salida = str(reserva['fecha_salida'])

            fecha_entrada_dt = datetime.strptime(fecha_entrada[:-4], '%a, %d %b %Y %H:%M:%S')
            fecha_salida_dt = datetime.strptime(fecha_salida[:-4], '%a, %d %b %Y %H:%M:%S')

            dia_nombre_entrada = fecha_entrada_dt.strftime('%A')
            dia_numero_entrada = fecha_entrada_dt.day
            mes_entrada = fecha_entrada_dt.strftime('%B')
            año_entrada = fecha_entrada_dt.year

            dia_nombre_salida = fecha_salida_dt.strftime('%A')
            dia_numero_salida = fecha_salida_dt.day
            mes_salida = fecha_salida_dt.strftime('%B')
            año_salida = fecha_salida_dt.year

            fecha_entrada_formateada = f"{dias_ES[dia_nombre_entrada]}, {dia_numero_entrada} de {meses_ES[mes_entrada]} {año_entrada}"
            fecha_salida_formateada = f"{dias_ES[dia_nombre_salida]}, {dia_numero_salida} de {meses_ES[mes_salida]} {año_salida}"

            reservas_historial.append({
                'fecha_entrada': fecha_entrada_formateada,
                'fecha_salida': fecha_salida_formateada,
                'hotel_nombre': hotel_datos['nombre'],
                'habitacion_nombre': habitacion_datos['nombre']
            })
    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500
    
    return render_template("perfil.html", usuario_datos = usuario_datos, reservas_historial = reservas_historial)


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
