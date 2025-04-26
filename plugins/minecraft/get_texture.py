from PIL import Image

from os import listdir
from os.path import isfile, join

def list_files_in_dir(_path):
    return [f for f in listdir(_path) if isfile(join(_path, f))]

path = "C:/Users/Jonatan/Documents/Coding/divoom-screen/plugins/minecraft/textures/items/"

files = list_files_in_dir(path)

#print(files)

#img = Image.open(path)


i = 0


def next_image():
    global i

    i += 1
    while not "png" in files[i]:
        i += 1

    _img = path + files[i]
    return _img

def open_image(_path):
    img = Image.open(_path)

    img = img.convert('RGBA')
    return img

def render():
    p = next_image()
    img = open_image(p)
    return(img)