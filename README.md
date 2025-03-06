# NTU CS/CZ4171 IoT Communications and Networking

Demo of project:\
https://youtu.be/qUYd8dFTbM4\

This project is a Python-based server that uses facial recognition to identify faces in images sent by clients. It receives an image, performs facial recognition, and returns the names of the recognized faces.

# Features:
Image Reception: The server receives images from a client over a socket connection.\
Facial Recognition: It uses the face_recognition library to identify faces in the received image.\
Socket Communication: The server communicates with the client using sockets, sending back recognized face names.

# How it works:
Server Setup: The server listens for incoming connections from clients on port 5005.\
python facial_recognition_server.py\
Image Reception: Once a connection is made, the server receives an image file in byte format from the client.\
Face Recognition: The server performs facial recognition on the received image using the known face encodings loaded from encodings.pickle.\
Response: The server sends back the names of the recognized faces (if any).
