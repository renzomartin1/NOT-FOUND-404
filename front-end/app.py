from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:5005/api"
PORT = 5001

app = Flask(__name__)
app.secret_key = "Not-Found-404-Grupo-17"


@app.route("/", methods = ["GET", "POST"])
def home():
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")
    cantidad_personas = request.args.get("cantidad_personas")
    
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


    # Sistema de registro e ingreso

    forzar_modal_register = False
    forzar_modal_login = False
    error_modal_register = ""
    error_modal_login = ""
    success_modal_login = ""

    if request.method == "POST":
        previous_url = request.referrer or url_for('home')  #Referrer es la URL anterior a la actual, si no existe devuelve la de home
        if len(request.form) == 6:
            contraseña = request.form.get("fr-contraseña")
            repetir_contraseña = request.form.get("fr-repetir-contraseña")

            if repetir_contraseña != contraseña:
                forzar_modal_register = True
                error_modal_register = "Las contraseñas no coinciden."

            else:
                datos_register = {
                    "nombre": request.form.get("fr-nombre"),
                    "apellido": request.form.get("fr-apellido"),
                    "email": request.form.get("fr-email"),
                    "telefono": request.form.get("fr-telefono"),
                    "contraseña": request.form.get("fr-contraseña")
                }

                try:
                    respuesta_api = requests.post(f"{API_URL}/usuarios/register", json = datos_register)
                except requests.exceptions.RequestException as error:
                    return jsonify({"error": str(error)}), 500

                if respuesta_api.status_code == 201:
                    json_api = respuesta_api.json()
                    forzar_modal_login = True
                    success_modal_login = json_api["success"]

                elif respuesta_api.status_code == 400:
                    json_api = respuesta_api.json()
                    forzar_modal_register = True
                    error_modal_register = json_api["error"]

        elif len(request.form) == 2:

            datos_login = {
                "email": request.form.get("fl-email"),
                "contraseña": request.form.get("fl-contraseña")
            }

            try:
                respuesta_api = requests.post(f"{API_URL}/usuarios/login", json = datos_login)
            except requests.exceptions.RequestException as error:
                return jsonify({"error": str(error)}), 500

            if respuesta_api.status_code == 400 or respuesta_api.status_code == 404:
                json_api = respuesta_api.json()
                forzar_modal_login = True
                error_modal_login = json_api["error"]

            elif respuesta_api.status_code == 200:
                json_api = respuesta_api.json()
                session["usuario_id"] = json_api["usuario_id"]
                return redirect(previous_url)


    return render_template("home.html", hoteles=hoteles, fecha_actual=fecha_actual, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, cantidad_personas=cantidad_personas,
    forzar_modal_register = forzar_modal_register, forzar_modal_login = forzar_modal_login, error_modal_register = error_modal_register, error_modal_login = error_modal_login, success_modal_login = success_modal_login)


@app.route("/logout")
def logout():
    session.pop("usuario_id")
    return redirect(url_for("home"))


@app.route("/hotel/<int:hotel_id>")
def hotel(hotel_id, fecha_entrada=None, fecha_salida=None, cantidad_personas=None): 
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")
    cantidad_personas = request.args.get("cantidad_personas")
    fecha_actual=datetime.now().strftime("%Y-%m-%d")

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
        hotel["servicios"] = hotel["servicios"].split(", ")
        if not habitaciones:
            return render_template("hotel.html", hotel=hotel, habitaciones=[], fecha_actual=fecha_actual)
    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return render_template("hotel.html", hotel=hotel, habitaciones=habitaciones, fecha_actual=fecha_actual)


@app.route("/habitacion/<int:habitacion_id>")
def habitacion(habitacion_id):
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")
    fecha_actual=datetime.now().strftime("%Y-%m-%d")
    try:
        response = requests.get(API_URL + '/habitacion/' + str(habitacion_id))
        response.raise_for_status()
        result = response.json()
        habitacion = result['habitacion']
        hotel = result['hotel']
        otras_habitaciones = result['otras_habitaciones']
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    return render_template("habitacion.html", habitacion=habitacion, otras_habitaciones=otras_habitaciones, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, hotel=hotel, fecha_actual=fecha_actual)


@app.route("/confirmacion_compra/<int:habitacion_id>")
def comprar(habitacion_id):

    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")

    fecha_entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")
    fecha_salida_dt = datetime.strptime(fecha_salida, "%Y-%m-%d")

    forzar_modal_login = False

    try:
        response = requests.get(API_URL + '/habitacion/' + str(habitacion_id))
        response.raise_for_status()
        response_disponible = requests.get(API_URL + '/reservas_habitacion/' + str(habitacion_id), params={'fecha_entrada': fecha_entrada, 'fecha_salida': fecha_salida})
        response_disponible.raise_for_status()

        result = response.json()
        habitacion = result['habitacion']
        hotel = result['hotel']
        otras_habitaciones = result['otras_habitaciones']
        reservas = response_disponible.json()
        #Si la habitacion ya esta reservada en esa fecha, no te deja reservarla
        for reserva in reservas:
           if fecha_entrada_dt < datetime.strptime(reserva['fecha_salida'], "%a, %d %b %Y %H:%M:%S GMT") and fecha_salida_dt > datetime.strptime(reserva['fecha_entrada'], "%a, %d %b %Y %H:%M:%S GMT"):
                error_reserva = "La habitación no está disponible en las fechas seleccionadas."
                return render_template("habitacion.html",habitacion=habitacion, otras_habitaciones=otras_habitaciones, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, hotel=hotel, error_reserva=error_reserva)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

    # Verificar si el usuario está logueado
    if "usuario_id" not in session:
        forzar_modal_login = True
        return render_template( "habitacion.html",habitacion=habitacion, otras_habitaciones=otras_habitaciones, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida, hotel=hotel,forzar_modal_login=forzar_modal_login)

    return render_template( "confirmacion_compra.html",habitacion=habitacion, fecha_entrada=fecha_entrada,fecha_salida=fecha_salida, forzar_modal_login=forzar_modal_login,hotel=hotel)



@app.route("/confirmacion_compra/reserva", methods = ["POST"])
def reserva_compra():
    usuario_id = int(request.form.get("usuario_id"))
    hotel_id = int(request.form.get("hotel_id"))
    habitacion_id = int(request.form.get("habitacion_id"))
    fecha_entrada = request.form.get("fecha_entrada")
    fecha_salida = request.form.get("fecha_salida")
    servicios_contratados = None
    fecha_creacion = datetime.now().strftime("%Y-%m-%d")

    reserva = {
        "usuario_id": usuario_id,
        "hotel_id": hotel_id,
        "habitacion_id": habitacion_id,
        "fecha_entrada": fecha_entrada,
        "fecha_salida": fecha_salida,
        "servicios_contratados": servicios_contratados,
        "fecha_creacion": fecha_creacion
    }

    try:
        response = requests.post(f'{API_URL}/reservas', json=reserva)
        if response.status_code == 201:
            return redirect(url_for('perfil', usuario_id=session["usuario_id"]))
        else:
            return jsonify({"error": "Error al crear la reserva"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500



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

            reserva_id = reserva['reserva_id']
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

            servicios_contratados = reserva['servicios']

            reservas_historial.append({
                'fecha_entrada': fecha_entrada_formateada,
                'fecha_salida': fecha_salida_formateada,
                'hotel_nombre': hotel_datos['nombre'],
                'habitacion_nombre': habitacion_datos['nombre'],
                'servicios_contratados': servicios_contratados,
                'reserva_id': reserva_id
            })

    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500
    
    return render_template("perfil.html", usuario_datos = usuario_datos, reservas_historial = reservas_historial, usuario_id = usuario_id)


@app.route("/eliminar_reserva/<int:reserva_id>")
def eliminar_reserva(reserva_id):
    try:
        response = requests.delete(f"{API_URL}/reservas/{reserva_id}")
        if response.status_code == 200:
            return redirect(url_for("perfil", usuario_id=session["usuario_id"]))
        else:
            return redirect(url_for("error_404"))
    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500


@app.route("/eliminar-cuenta/<int:usuario_id>")
def eliminar_cuenta(usuario_id):
    try:
        response = requests.delete(f"{API_URL}/usuarios/{usuario_id}")
        if response.status_code == 200:
            return redirect(url_for("logout"))
        else:
            return redirect(url_for("error_404"))
    except requests.exceptions.RequestException as e:
        return jsonify({ 'error': str(e) }), 500


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
