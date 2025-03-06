# stop_event = Event()
from threading import Condition
from http import server
import face_recognition
import numpy as np
import cv2
import pickle
import io


encodingsP = "encodings.pickle"
data = pickle.loads(open(encodingsP, "rb").read())

# Load known face encodings and their names
with open('encodings.pickle', 'rb') as file:
    known_face_encodings = pickle.load(file)['encodings']
    # known_face_names = pickle.load(file)['names']
    known_face_names = data['names']

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
        self.face_detected = False
        self.face_name = "Unknown"

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, process for face recognition
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                # Ensure the frame is not empty
                if len(self.frame) > 0:
                    self.condition.notify_all()
                    # Convert buffer to numpy array
                    data = np.frombuffer(self.frame, dtype=np.uint8)
                    # Check if data is not empty to avoid imdecode error
                    if data.size > 0:
                        # Decode image
                        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
                        # Check if the image was successfully decoded
                        if image is not None:
                            # Perform face recognition
                            image = self.process_frame(image)
                            # Check if a face was recognized
                            # if self.face_recognized:
                                # print("in write", self.face_recognized)
                                # return False

                                # Set the flag to stop the camera
                                # self.face_recognized = False
                            # self.face_recognised

                            # Re-encode the image after processing
                            _, buffer = cv2.imencode('.jpg', image)
                            self.frame = buffer.tobytes()
                self.buffer.seek(0)
        return self.buffer.write(buf)
    
    # def process_frame(self, image):

    #     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     face_names = []
    #     # rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     small_rgb_image = cv2.resize(rgb_image, (0, 0), fx=0.25, fy=0.25)
    #     rgb_small_frame = small_rgb_image[:, :, ::-1]
    #     try:
    #             # Find all the faces and face encodings in the current frame of video
    #         face_locations = face_recognition.face_locations(small_rgb_image)
    #         face_encodings = face_recognition.face_encodings(small_rgb_image, face_locations)
    #     except Exception as e:
    #         print("error is e")

    #     counter = 0
    #     threshold = 0.5
    #     name = "Unknown"
    #     if not face_locations:
    #         face_names.append(name)
    #         self.face_name = name

    #     #  matches = face_recognition.compare_faces(data["encodings"], face_encoding)
    #     for face_encoding in face_encodings:
    #      face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    #      best_match_index = np.argmin(face_distances)
    #      matches_within_threshold = np.where(face_distances <= threshold)[0]
    #      print("matches_within_threshold", matches_within_threshold, best_match_index, face_distances)
    #      if len(matches_within_threshold) > 0:
    #         best_match_index = matches_within_threshold[np.argmin(face_distances[matches_within_threshold])]
    #         print(f"Best match index within threshold: {best_match_index}")
    #         id,name = known_face_names[best_match_index].split('_',1)
    #      else:
    #         name = "Unknown"
    #      face_names.append(name)
    #      self.face_name = name
        
    #     #  print("face_names", name)
    #     #  if matches[best_match_index]:
    #         # name = known_face_names[best_match_index]
    #     # print("No match within threshold.")
    #     # print("best_match_index", best_match_index )
    #     #  if matches[best_match_index]:
    #     #      id,name = known_face_names[best_match_index].split('_',1)
    #     #      # name = known_face_names[best_match_index]


    #     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    #         # See if the face is a match for the known face(s)
    #         top *= 4
    #         right *= 4
    #         bottom *= 4
    #         left *= 4
    #         # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    #         # name = "Unknown"

    #         # Draw a box around the face
    #         cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

    #         # Draw a label with a name below the face
    #         cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
    #         # font = cv2.FONT_HERSHEY_DUPLEX
    #         font = cv2.FONT_HERSHEY_SIMPLEX

    #         cv2.putText(image, name, (left + 6, bottom - 6), font, 0.6, (0, 0, 10), 1)

    #     if name != "Unknown":
    #         self.face_detected = True
    #         # print("in process", self.face_recognized)
    #         # subprocess.run(["python", "app_return.py"])
    #     return image


    def process_frame(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_names = []
        small_rgb_image = cv2.resize(rgb_image, (0, 0), fx=0.25, fy=0.25)
        try:
            face_locations = face_recognition.face_locations(small_rgb_image)
            face_encodings = face_recognition.face_encodings(small_rgb_image, face_locations)
        except Exception as e:
            print("error is e")
        threshold = 0.5
        name = "Unknown"
        if not face_locations:
            face_names.append(name)
            self.face_name = name
        for face_encoding in face_encodings:
         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
         matches_within_threshold = np.where(face_distances <= threshold)[0]
         if len(matches_within_threshold) > 0:
            best_match_index = matches_within_threshold[np.argmin(face_distances[matches_within_threshold])]
            id,name = known_face_names[best_match_index].split('_',1)
         else:
            name = "Unknown"
         face_names.append(name)
         self.face_name = name
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            # label below the face
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 0.6, (0, 0, 10), 1)
        if name != "Unknown":
            self.face_recognized = True
        return image