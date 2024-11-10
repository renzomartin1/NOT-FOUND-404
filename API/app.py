from flask import Flask, jsonify, request

import querys

app = Flask(__name__)


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)