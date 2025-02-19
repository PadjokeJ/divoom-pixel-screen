from pyautogui import screenshot
from PIL import Image

def screenshot_to_16x(bounds=None):
    screen = screenshot()
    size = screen.size

    if bounds is None:
        bounds = center_screenshot(size)
    
    img = screen.crop(bounds)

    return img.resize((16, 16))

def center_screenshot(size):
    w, h = size

    if w > h:
        start = (w - h) // 2
        crop_box = (start, 0, start + h, h)
    else:
        start = (h - w) // 2
        crop_box = (0, start, w, start + w)
    
    return crop_box
