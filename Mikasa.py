#1202118395400249932603
#6152731477407697949540
#6372166874982901333702
#2567022535702469160698
#6475120608577753120200

import cv2
import numpy as np
import win32api
import threading
from rzctl import RZCONTROL, MOUSE_CLICK
import bettercam
import time


#UUID = "e81036d1e9184ea68b533b82bd8208a8"  
#8877336546119821861253
#UUID = "e81036d1e9184ea68b533b82bd8208a8"  

print("BETTER PVP")

camera = bettercam.create()
lock = threading.Lock()


fovX = 50
fovY = 50
cor = "purple"
offsetY = 5
smooth = 2
MOVE_THRESHOLD = 3
resolutionX = win32api.GetSystemMetrics(0)
resolutionY = win32api.GetSystemMetrics(1)

left = (resolutionX - fovX) // 2
top = (resolutionY - fovY) // 2
right = left + fovX
bottom = top + fovY
region = (left, top, right, bottom)

#3571536452104542858556
#7635516097024640624653

color_conditions = {
    "purple": lambda r, g, b: np.logical_and.reduce(
        (np.abs(r - b) <= 30, r - g >= 60, b - g >= 60, r >= 140, b >= 170, g < b))
}


AOT = RZCONTROL()
if not AOT.init():
    print("Failed to initialize AOT")
    

#7044946056237116553249
#7393237487428626095145
def megumin():
    with lock:
        frame = camera.grab(region=region)
        if frame is None:
            return
        
        b, g, r = cv2.split(frame)
        condition = color_conditions[cor]
        mask = condition(r, g, b).astype(np.uint8) * 255
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        if contours:
            screen_center = (fovX // 2, fovY // 2)
            min_distance = float('inf')
            closest_contour = None

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                distance = ((center[0] - screen_center[0]) ** 2 + (center[1] - screen_center[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour
            
            if closest_contour is not None:
                x, y, w, h = cv2.boundingRect(closest_contour)
                target_y = y + int(h * 0.15)
                cX = x + w // 2
                cY = target_y
                x_diff = cX - (fovX // 2)
                y_diff = cY - (fovY // 2) + offsetY
                
                if abs(x_diff) <= MOVE_THRESHOLD and abs(y_diff) <= MOVE_THRESHOLD:
                    AOT.mouse_click(MOUSE_CLICK.LEFT_DOWN)
                    time.sleep(0.01)
                    AOT.mouse_click(MOUSE_CLICK.LEFT_UP)
                else:
                    AOT.mouse_move(int(x_diff), int(y_diff), smooth, True)
                
#4370280007047973890183
#8187759279071809792235

megumin_thread = threading.Thread(target=megumin)
megumin_thread.daemon = True
megumin_thread.start()

if __name__ == "__main__":
    while True:
        if win32api.GetAsyncKeyState(18):
            megumin()
        time.sleep(0.001)
        

#5442415760088143371826
#1072804571341486221430
#9711086728809833772701
#9650172390476874996158
#4401980925008365522344
