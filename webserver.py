import pixoo as px
from PIL import Image
from io import BytesIO
from time import sleep

from os import getenv
from dotenv import load_dotenv

load_dotenv("local.env", verbose=True)
mac_address = getenv("MAC_ADDRESS")

import threading

from flask import Flask, request
app = Flask(__name__)




def init_connection(): # This will have to run on another thread since one thread can't handle 2 sockets
    pixoo = px.Pixoo(mac_address)
    pixoo.connect()
    while True:
        try:pixoo.draw_pic('tmp.png')
        except:pass
        sleep(0.1)


@app.route('/update-screen', methods=['POST'])
def update_screen():
    try:
        file = request.files.get("file")

        byteImg = file.read()

        tmp = Image.open(BytesIO(byteImg))
        tmp.save('tmp.png')

        return {}, 200
    except Exception as e:
        return {"message" : f"An error occurred -> {e}"}, 403

if __name__ == "__main__":
    threading.Thread(target=init_connection).start()
    ip = "0.0.0.0"  # makes the webserver accessible to other devices on the same network
    app.run(host=ip, debug=True)
