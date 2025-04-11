from flask import Flask, render_template, request
from flask_cors import CORS

from PIL import Image, ImageDraw

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "Hello world!"}

@app.route("/send", methods=["GET"])
def send():
    message = request.args.get('message', "")
    with open("message.txt", "w") as f:
        f.write(message)

    return {"message": message}

if __name__ == ("__main__"):
    app.run(host="0.0.0.0", debug=True)