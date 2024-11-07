from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/confirmacion-compra")
def comprar():
    return render_template("confirmacion_compra.html")


if __name__ == "__main__":
    app.run(debug = True, port = 8080)