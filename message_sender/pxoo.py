import pixoo
from os import getenv
from dotenv import load_dotenv

from time import sleep
from PIL import Image, ImageDraw, ImageFont


if __name__ == "__main__":
    load_dotenv("local.env", verbose=True)

    bt_mac_addr = getenv("BT_MAC_ADDR")
    tmp_folder = getenv("TEMP_FOLDER")
    
    assert bt_mac_addr is not None, "Did you copy the example.env to local.env?"
    assert tmp_folder is not None, "Did you copy the example.env to local.env?"

    print(bt_mac_addr)
    p = pixoo.Pixoo(bt_mac_addr)
    p.connect()
    
    while True:
        message = ""
        with open("message.txt", "r") as f:
            message = f.readline()
        x = 16
        max_x = 100
        while True:
            x -= 1
            if x < -max_x:
                break
            image = Image.new("RGB", (16, 16))
            draw = ImageDraw.Draw(image)
            max_x = draw.textlength(message, draw.font)
            draw.text((x, 2), message, "#ff0055")

            try: p.draw_pic_from_PIL(image)
            except Exception as e:
                print(e)
                p.connect()
            sleep(0.1)  # 10 fps are already pretty smooth