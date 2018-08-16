import io
import socket
import struct
import numpy as np
import cv2
import time

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
print("client connected....")
count = 0
try:
    cv2.namedWindow('feed', cv2.WINDOW_NORMAL)
    start = time.time()
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            print("0 sent")
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        print(image_len)
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1).reshape(1280, 1024, 3)
        cv2.imshow('feed', image)
        cv2.waitKey(3)
        count += 1
finally:
    connection.close()
    server_socket.close()
    cv2.destroyAllWindows()
    end = time.time()
    print("receiving FPS = ", count/(end - start))
