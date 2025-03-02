from os import getenv
from time import sleep
from PIL import Image
from dotenv import load_dotenv
import screenshot_display

import pixoo as pixc

load_dotenv("local.env", verbose=True)

green = (50, 255, 50, 255)
red = (150, 50, 50, 255)

if __name__ == "__main__":
    bt_mac_addr = getenv("BT_MAC_ADDR")
    tmp_folder = getenv("TEMP_FOLDER")
    spotify_token = getenv("SPOTIFY_TOKEN")
    assert bt_mac_addr is not None, "Did you copy the example.env to local.env?"
    assert tmp_folder is not None, "Did you copy the example.env to local.env?"

    print(bt_mac_addr)
    pixoo = pixc.Pixoo(bt_mac_addr)
    pixoo.connect()
    
    

    while True:  # Main loop - here you can change the drawing functions
        
        img = screenshot_display.screenshot_to_16x((1620, 780, 1920, 1080)).convert("RGBA")
        try: pixoo.draw_pic_from_PIL(img)
        except Exception as e: pixoo.connect()

        sleep(0.1)  # 10 fps are already pretty smooth
        