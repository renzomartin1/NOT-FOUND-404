from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    #ejemplo de hoteles
    hoteles = [
        {
            "name": "Hotel Paradise",
            "location": "Miami, FL",
            "description": "A luxurious hotel located by the beach with stunning ocean views.",
            "images": [
                "https://imgs.search.brave.com/HPsF4UChA100XcJBrN2WC0xy3iy0GXwEK2E4V9jpitk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/Zm90b3MtcHJlbWl1/bS9yZWNlcGNpb24t/by1jaGVjay1pbi1l/bGVnYW50ZS1tb2Rl/cm5vLWhvdGVsLW5l/Z29jaW9zXzEyMDY0/MTMtMTU4MDkuanBn/P3NlbXQ9YWlzX2h5/YnJpZA",
                "https://example.com/hotel_paradise_2.jpg",
                "https://example.com/hotel_paradise_3.jpg"
            ]
        },
        {
            "name": "Mountain Retreat",
            "location": "Aspen, CO",
            "description": "A cozy hotel in the heart of the mountains, perfect for a winter getaway.",
            "images": [
                "https://imgs.search.brave.com/mPXdl9oWtxE3GeTTPM3TnMlL0W51u5xGTXU6yED-wgg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/Zm90b3MtcHJlbWl1/bS9lc2NlbmEtcGVy/c29uYWwtbWFudGVu/aW1pZW50by1ob3Rl/bC1yZWFsaXphbmRv/LWNvbXByb2JhY2lv/bmVzLXJlcGFyYWNp/b25lcy1ydXRpbmFf/OTk1NTc4LTE3NTMw/LmpwZz9zaXplPTYy/NiZleHQ9anBn",
                "https://example.com/mountain_retreat_2.jpg",
                "https://example.com/mountain_retreat_3.jpg"
            ]
        },
        {
            "name": "City Lights Hotel",
            "location": "New York, NY",
            "description": "An upscale hotel in downtown New York with easy access to attractions.",
            "images": [
                "https://imgs.search.brave.com/idA0nPT7rbZzH2WHwFiFsnvaI27Fd17l7fKrX4xskjU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/Zm90b3MtcHJlbWl1/bS92ZW50YXMtY29t/ZXJjaWFsaXphY2lv/bi1ob3RlbGVzXzEz/MTQ0NjctNzk0ODEu/anBnP3NpemU9NjI2/JmV4dD1qcGc",
                "https://example.com/city_lights_2.jpg",
                "https://example.com/city_lights_3.jpg"
            ]
        },
        {
            "name": "Desert Oasis",
            "location": "Las Vegas, NV",
            "description": "An exotic hotel with desert views and a large casino.",
            "images": [
                "https://images.unsplash.com/photo-1549294413-26f195200c16?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8aG90ZWx8ZW58MHx8MHx8fDA%3D",
                "https://example.com/desert_oasis_2.jpg",
                "https://example.com/desert_oasis_3.jpg"
            ]
        }
    ]
    return render_template("home.html", hoteles=hoteles)

@app.route("/confirmacion-compra")
def comprar():
    return render_template("confirmacion_compra.html")


if __name__ == "__main__":
    app.run(debug = True, port = 8080)
