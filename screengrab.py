from mss.linux import MSS as mss
import cv2
import numpy as np
import time

sct = mss()
monitor_number = 2
mon = sct.monitors[monitor_number]
print(mon["width"], mon["height"])

monitor = {
    "top":mon["top"],
    "left":mon["left"],
    "width":mon["width"],
    "height":mon["height"],
    "mon":monitor_number,
}

cv2.namedWindow('feed', cv2.WINDOW_NORMAL)
count = 0
start = time.time()
try:
    while True:
        sct_img = sct.grab(monitor)
        image_bytes = sct_img.rgb
        image = np.fromstring(image_bytes, dtype=np.uint8).reshape(1280, 1024, 3)
        cv2.imshow('feed', image)
        count+=1
        if cv2.waitKey(4) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
finally:
    end = time.time()
    print("FPS = ", count/(end-start))
