from os import getenv
from time import sleep
from PIL import Image
from dotenv import load_dotenv

from pixoo import Pixoo as Pixoo16x

load_dotenv("local.env", verbose=True)

if __name__ == "__main__":
    bt_mac_addr = getenv("BT_MAC_ADDR")
    tmp_folder = getenv("TEMP_FOLDER")
    
    assert bt_mac_addr is not None, "Did you copy the example.env to local.env?"
    assert tmp_folder is not None, "Did you copy the example.env to local.env?"

    print(bt_mac_addr)
    pixoo = Pixoo16x(bt_mac_addr)

    pixoo.connect()

    img = Image.new("RGBA", (16, 16))
    
    while True:
        try: # sometimes errors happen while trying to draw the picture 
            pixoo.draw_pic_from_PIL(img) 
        except Exception as e: # print exception and attempt reconnecting to screen
            print(e)
            pixoo.connect()
        sleep(0.1)  # 10 fps are already pretty smooth -> avoids overloading the screen with requests