from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import mysql.connector
import requests

URL = "https://nmendozab.pythonanywhere.com/api/"
#Window.size = (400, 840)


class Hotelisco(App):
    def build(self):
        
        Builder.load_file('templates/main.kv')  
        sm = ScreenManager()

    
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(Reservas(name="reservas"))
        sm.add_widget(Servicios(name="servicios"))
        sm.add_widget(Contrataciones(name="contrataciones"))

        sm.current = "login"  # Establecer la pantalla inicial

        return sm

    
    def verificar_usuario(self):
        email = self.root.get_screen("login").ids.email.text
        contraseña = self.root.get_screen("login").ids.contraseña.text
        data = {"email": email, "contraseña": contraseña}

        try:
            response = requests.post(URL + "verificar_usuario", json=data)

            if response.status_code == 200:
                usuario_id = response.json().get("usuario_id")
                self.root.get_screen("reservas").usuario_id = usuario_id
                self.root.current = "reservas"
            else:
                self.root.get_screen("login").ids.message.text = response.json().get("message", "Error desconocido.")
        except requests.RequestException as err:
            self.root.get_screen("login").ids.message.text = f"Error al conectar con el servidor: {err}"

    def logout(self):
        self.root.current = "login"

    def volver_atras(self, instance):
        self.root.current = "reservas"

    def verificar_reserva(self, usuario_id, reserva_id):
        data = {"reserva_id": reserva_id, "usuario_id": usuario_id}	
        try:
            response = requests.post(URL + "verificar_reserva", json=data)

            if response.status_code == 200:
                nueva_reserva_id = response.json().get("usuario_id")
                self.root.get_screen("servicios").reserva_id = nueva_reserva_id
                self.root.get_screen("servicios").usuario_id = usuario_id
                self.root.current = "servicios"
            else:
                self.root.get_screen("reservas").ids.message.text = response.json().get("message", "Error desconocido.")
        except requests.RequestException as err:
            self.root.get_screen("reservas").ids.message.text = f"Error al conectar con el servidor: {err}"
    
class LoginScreen(Screen):
    pass

class Reservas(Screen):
    usuario_id = None

    def on_enter(self):
        self.ids.message.text = "Bienvenido. Ingresa tu ID de reserva."

    #Se encarga de traer el reserva_id que escribio el usuario
    def validar_reserva(self): 
        reserva_id = self.ids.reserva_id.text
        
        if not reserva_id:
            self.ids.message.text = "Por favor ingrese un ID de reserva."
            return
        
        # Validar si la reserva existe y está asociada al usuario
        result = App.get_running_app().verificar_reserva(self.usuario_id, reserva_id)

        if not result:
            self.ids.message.text = "No se encontró una reserva con ese ID para el usuario."
            return


class Servicios(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usuario_id = None
        self.reserva_id = None
        self.checkboxes = []
        self.labels = []  
    
    def obtener_servicios(self):
        servicios_json = {}
        data = {"reserva_id": self.reserva_id, "usuario_id": self.usuario_id}
        try:
            response_hotel_id = requests.post(f"{URL}verificar_reserva", json=data)
            if response_hotel_id.status_code == 200:
                hotel_id = response_hotel_id.json().get("hotel_id")
                response_servicios = requests.get(f"{URL}hoteles/servicios/{hotel_id}")
                if response_servicios.status_code == 200:
                    servicios_json = response_servicios.json()
                else:
                    print(f"Error: No se pudo obtener los servicios, {response_servicios.status_code}")
            else:
                print(f"Error: No se pudo obtener el hotel_id, {response_hotel_id.status_code}")

        except Exception as e:
            print(f"Error al obtener los servicios: {e}")
        
        if "servicios" in servicios_json:
            lista_servicios = servicios_json["servicios"].split(", ")
        else:
                lista_servicios = []
        return lista_servicios  
