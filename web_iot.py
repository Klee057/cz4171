import json
import signal
from threading import Thread
import threading
import time
from http import server
# import facepart
import logging
import socketserver
import io
import subprocess
import picamera
from threading import Condition, Timer
import socket

# Server address and port
SERVER_IP = 'xxx.xxx.xx.xxx'
SERVER_PORT = 5005

# Initialize PiCamera
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    # print("Camera initialized.")
    # camera.start_preview()
    # Camera warm-up time
    time.sleep(2)

    # Capture to in-memory stream
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    image_data = stream.getvalue()
    # print("Image captured.")

# Create a socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

try:
    # send = 3
    # Send image size and data
    # while send:
    client_socket.sendall(len(image_data).to_bytes(4, 'big'))
    client_socket.sendall(image_data)
        # send -= 1
        # time.sleep(2)
    # print("Image has been sent successfully.")
    response = client_socket.recv(1024)
    print("Response from server:", response.decode())


finally:
    client_socket.close()

#cd ~/project && source env/bin/activate && cd facial-recognition2

# output = facepart.StreamingOutput()
# run_server()

