import io
import socket
import struct
import time
import cv2
from mss.linux import MSS as mss
import numpy as np

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('0.0.0.0', 8000))
print("server found....")

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
# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
count = 0
try:
    #camera = picamera.PiCamera()
    #camera.resolution = (640, 480)
    # Start a preview and let the camera warm up for 2 seconds
    #camera.start_preview()
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    # video_path = "/home/aditya/Documents/leisure/desktoppy/Movies/10HON_tank.avi"
    # video = cv2.VideoCapture(video_path)
    start = time.time()

    while True:
        # ok, frame = video.read()
        # if not ok:
        #     break
        ####### new code to take screen shot - comment everything upward ############

        sct_img = sct.grab(monitor)
        image_bytes = sct_img.rgb
        frame = np.fromstring(image_bytes, dtype=np.uint8).reshape(1280, 1024, 3)
        encoded, frame = cv2.imencode('.jpg', frame)
        frame = bytes(frame)
        #print(frame)
        stream = io.BytesIO(frame)
        stream.seek(0, 2)
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        # If we've been capturing for more than 30 seconds, quit
        # if time.time() - start > 30:
        #     break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        count += 1
    # Write a length of zero to the stream to signal we're done
    print("0 sent")
    connection.write(struct.pack('<L', 0))
except KeyboardInterrupt:
    connection.write(struct.pack('<L', 0))
finally:
    end = time.time()
    print("Sending FPS = ", count/(end-start))
    connection.close()
    client_socket.close()

