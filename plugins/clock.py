from copy import copy
import os
from time import sleep
from PIL import Image

import math
import datetime

def cls(s):
    for x in range(len(s)):
        for y in range(len(s)):
            s[x][y] = 0
    return s

# 
def render(img, s):
    p = img.load()
    for x in range(len(s)):
        for y in range(len(s)):
            match s[x][y]:
                case 0:
                    p[x, y] = (0, 0, 0, 255)
                case 1:
                    p[x, y] = (200, 20, 80, 255)
                case 2:
                    p[x, y] = (150, 20, 150, 255)
                case 3:
                    p[x, y] = (80, 20, 200, 255)

def clear(s, dim):
    for x in dim:
        for y in dim:
            s[x][y] = 0
        
        
def bresenham(s, dx, dy , color):
    x0, x1 = 7, 7 + round(dx)
    y0, y1 = 7, 7 + round(dy)
    
    dx = abs(dx)
    sx = -1
    if x0 < x1:
        sx = 1
    dy = -abs(dy)
    sy = -1
    if y0 < y1:
        sy = 1
    error = dx + dy
    
    while True:
        s[x0][y0] = color
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error += dy
            x0 += sx
        if e2 <= dx:
            if y0 == y1:
                break
            error += dx
            y0 += sy
#


def plot_hands(screen):
    
    now = datetime.datetime.now().time()
    
    s = now.second
    print(s)

    s = s / 60
    dx = math.cos(math.pi * (s - 0.25) * 2) * 7.5
    dy = math.sin(math.pi * (s - 0.25) * 2) * 7.5
    bresenham(screen, dx, dy, 1)
        
    m = now.minute
    print(m)
    m = m / 60
    

    dx = math.cos(math.pi * (m - 0.25) * 2) * 6
    dy = math.sin(math.pi * (m - 0.25) * 2) * 6
    bresenham(screen, dx, dy, 2)
    
    h = now.hour
    print(h)
    h = (h + m) / 12
    dx = math.cos(math.pi * (h - 0.25) * 2) * 4.5
    dy = math.sin(math.pi * (h - 0.25) * 2) * 4.5
    bresenham(screen, dx, dy, 3)

def clock_main():
    # init screen
    col = [0 for i in range(16)]
    screen = [copy(col) for i in range(16)]
    screen[7][7] = 1

    scr = Image.new("RGBA", (16, 16))

    plot_hands(screen)

    render(scr, screen)

    return scr