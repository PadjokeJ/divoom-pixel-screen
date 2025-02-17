from os import getenv
from time import sleep
from PIL import Image
from dotenv import load_dotenv
import visualizer

import pixoo as pixc

load_dotenv("local.env", verbose=True)

green = (50, 255, 50, 255)
red = (150, 50, 50, 255)

if __name__ == "__main__":
    bt_mac_addr = getenv("BT_MAC_ADDR")
    tmp_folder = getenv("TEMP_FOLDER")
    
    assert bt_mac_addr is not None, "Did you copy the example.env to local.env?"
    assert tmp_folder is not None, "Did you copy the example.env to local.env?"

    print(bt_mac_addr)
    pixoo = pixc.Pixoo(bt_mac_addr)
    pixoo.connect()
    #base = Image.new("RGBA", (16, 16), (0, 0, 0, 255))  # Create a base new image

    #base = Image.open("placeholder.png")
    
    

    
    
    while True:  # Main loop - here you can change the drawing functions
        base = visualizer.plot_visualizer()


        base.save(tmp_folder + "tmp.png")
        try: pixoo.draw_pic(tmp_folder + "tmp.png")
        except Exception as e:
            print(e)
            pixoo.connect()
        sleep(0.1)  # 10 fps are already pretty smooth