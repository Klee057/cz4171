import os
import pickle
import socket
import subprocess
import face_recognition
import numpy as np
import cv2
import paramiko
# Server configuration
HOST = '0.0.0.0'
PORT = 5005
# ENCODING

import cv2
import numpy as np
import face_recognition

file_path = 'C:/Users/tokei/personal-projects/facial-recognition2/train_model_server.py'
with open(file_path, 'r') as file:
    code = file.read()
exec(code)

print("encoding done")
encodingsP = "encodings.pickle"
data = pickle.loads(open(encodingsP, "rb").read())
with open('encodings.pickle', 'rb') as file:
    known_face_encodings = pickle.load(file)['encodings']
    # known_face_names = pickle.load(file)['names']
    known_face_names = data['names']


import face_recognition

def recognize_faces_in_image(image_path, known_face_encodings, known_face_names):
    """
    Recognize faces in an image using known face encodings.

    Args:
    - image_path (str): Path to the image file.
    - known_face_encodings (list): List of known face encodings.
    - known_face_names (list): List of corresponding names for the known face encodings.

    Returns:
    - list: List of names of the recognized faces in the image.
    """
    # Load the image
    image = face_recognition.load_image_file(image_path)

    # Find all face locations and encodings in the image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    # Initialize an array for names of identified faces
    face_names = []
    threshold = 0.5
    name = "Unknown"
    if not face_locations:
        face_names.append(name)
    # Loop through each face found in the image
    for face_encoding in face_encodings:
        # Compare the face encoding with the known face encodings
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        matches_within_threshold = np.where(face_distances <= threshold)[0]

        # If a match is found, use the name from the known face names list
        if len(matches_within_threshold) > 0:
            best_match_index = matches_within_threshold[np.argmin(face_distances[matches_within_threshold])]
            id,name = known_face_names[best_match_index].split('_',1)
        else:
            name = "Unknown"
        face_names.append(name)

    return face_names






# with open('C:/Users/tokei/personal-projects/facial-recognition2/images_yG4j2ReTV0cN66NSVcEh_keith.jpg', 'rb') as file:
#     # Read the entire image file into bytes
#     image_size_data = file.read()

# Create a socket object
print("Creating socket...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server listening on port", PORT)
current_directory = os.getcwd()
# current_directory = os.path.join(os.getcwd(), 'facial-recognition2')
try:
    while True:
        # Accept a connection
        connection, addr = server_socket.accept()
        connection.settimeout(60)
        print('Connected by', addr)
        # Receive command from the client
        # command = connection.recv(1024).decode().strip()
        image_size_data = connection.recv(4) #######
        # image_size_data = len(image_data).to_bytes(4, 'big') ######
        # Receive data
        if not image_size_data:
            print("waiting to receive image size", image_size_data)
            continue
        image_size = int.from_bytes(image_size_data, 'big')
        image_data = b''

        while len(image_data) < image_size:
            packet = connection.recv(4096)
            if not packet:
                break
            image_data += packet

        # Write the data to a file
        file_name = 'iot_image.jpg'
        file_path = os.path.join(current_directory, file_name)
        print(current_directory)
        with open(file_path, 'wb') as f:
            f.write(image_data)
        print("Image received and saved. ", file_path)

        recognized_faces = recognize_faces_in_image(file_path, known_face_encodings, known_face_names)
        response = recognized_faces[0]
        connection.sendall(response.encode())

        print("Identified faces:", recognized_faces)
        continue
        # connection.close()
finally:
    server_socket.close()




