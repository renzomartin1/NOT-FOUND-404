from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
import mysql.connector

class LoginScreen(Screen):
    pass

class Reservas(Screen):
    usuario_id = None

    def on_enter(self):
        self.ids.message.text = "Bienvenido. Ingresa tu ID de reserva."

    def validar_reserva(self):
        reserva_id = self.ids.reserva_id.text
        
        if not reserva_id:
            self.ids.message.text = "Por favor ingrese un ID de reserva."
            return
        
        # Validar si la reserva existe y está asociada al usuario
        result = App.get_running_app().verificar_reserva(reserva_id, self.usuario_id)


        if result:
            servicios_screen = self.manager.get_screen("servicios")

            self.manager.current = "servicios"
        else:
            self.ids.message.text = "No se encontró una reserva con ese ID para el usuario."

class Servicios(Screen):
    def confirmar_servicios(self):

        servicios_seleccionados = []

        if self.ids.servicio_1.active:
            servicios_seleccionados.append("Servicio A")
        if self.ids.servicio_2.active:
            servicios_seleccionados.append("Servicio B")
        if self.ids.servicio_3.active:
            servicios_seleccionados.append("Servicio C")
        if self.ids.servicio_4.active:
            servicios_seleccionados.append("Servicio D")

        if servicios_seleccionados:
            # Aca tenemos que hacer para mostrar los servicios seleccionados
            self.ids.message.text = f"Servicios seleccionados: {', '.join(servicios_seleccionados)}"
        else:
            self.ids.message.text = "No se seleccionaron servicios."


class Hotelisco(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'

        return Builder.load_file("login.kv")

    def verificar_usuario(self):
        email = self.root.get_screen("login").ids.email.text
        contraseña = self.root.get_screen("login").ids.contraseña.text
        
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="hospedajes"
            )
            cursor = connection.cursor()

            # Consulta para verificar el usuario
            QUERY_TRAER_USUARIO_BY_EMAIL = "SELECT * FROM usuarios WHERE email = %s AND contraseña = %s"
            cursor.execute(QUERY_TRAER_USUARIO_BY_EMAIL, (email, contraseña))
            result = cursor.fetchone()

            if result:
                usuario_id = (result[0])
                self.root.get_screen("reservas").usuario_id = usuario_id
                self.root.current = "reservas"
            else:
                self.root.get_screen("login").ids.message.text = "Usuario o contraseña incorrectos."
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            self.root.get_screen("login").ids.message.text = f"Error: {err}"

    def logout(self):
        self.root.current = "login"

    def verificar_reserva(self, reserva_id, usuario_id):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="hospedajes"
            )
            cursor = connection.cursor()

            # Consulta para verificar si el usuario tiene esa reserva_id
            QUERY_RESERVA_BY_RESERVA_ID = "SELECT * FROM reservaciones WHERE usuario_id = %s AND reserva_id = %s"
            cursor.execute(QUERY_RESERVA_BY_RESERVA_ID, (usuario_id, reserva_id))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return result
        except mysql.connector.Error as err:
            return None



Hotelisco().run()