from os import getenv
from time import sleep
from PIL import Image
from dotenv import load_dotenv
import spotify_reader

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
    #base = Image.new("RGBA", (16, 16), (0, 0, 0, 255))  # Create a base new image

    #base = Image.open("placeholder.png")
    
    

    song = spotify_reader.progress_bar()
    dt = (song[1] - song[0]) / 1000.0
    print(dt)
    t = 0
    real_time = 0

    t_p = 0
    if song[3]: t_p = 0.1
    else: t_p = 0


    base = Image.open(spotify_reader.album_cover(song[2]))
    if base.mode != 'RGBA': base = base.convert('RGBA')
    base.save(tmp_folder + "tmp.png")
    base = base.resize((16, 16))

    size = width, height = base.size
    pixels = base.load()
    for pbx in range(width):
        pixels[pbx, 15] = (0, 0, 0, 255)

    while True:  # Main loop - here you can change the drawing functions
        if (real_time > 5 or dt - t < 0):
            song = spotify_reader.progress_bar()

            image_url = song[2]


            base = Image.open(spotify_reader.album_cover(image_url))
            if base.mode != 'RGBA': base = base.convert('RGBA')
            base = base.resize((16, 16))
            pixels = base.load()

            for pbx in range(width):
                pixels[pbx, 15] = (0, 0, 0, 255)


            dt = (song[1] - song[0]) / 1000.0
            t = 0
            real_time = 0
            if song[3]: t_p = 0.1
            else: t_p = 0
            print(dt)

        x = 0
        if t_p == 0: col = red
        else: col = green
        while x / float(width) < (song[0] + t * 1000) / song[1]:
            if x > 16:
                break
            pixels[max(x - 1, 0), 15] = col
            x += 1
            

        calc = 16 * (song[0] + t * 1000) / song[1]
        pixel_progress = calc - int(calc)
        x = min(x, 16)
        if song[3]:
            pixels[x - 1, 15] = (50, int(255 * pixel_progress), 50, 255)

        # workaround for final displaying
        base.save(tmp_folder + "tmp.png")
        try: pixoo.draw_pic(tmp_folder + "tmp.png")
        except Exception as e:
            print(e)
            pixoo.connect()
        sleep(0.1)  # 10 fps are already pretty smooth
        t += t_p
        real_time += 0.1