import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore


cred = credentials.Certificate('/home/pi/project/facial-recognition2/rpi-key.json')

firebase_admin.initialize_app(cred, {
    'storageBucket': 'rpiapp-17f72.appspot.com'
    })


def upload_to_storage(local_file_path, cloud_file_path):
    """
    Uploads a file to Firebase Cloud Storage.

    Args:
    local_file_path (str): The local path to the file.
    cloud_file_path (str): The desired cloud path including the filename.
    """
    bucket = storage.bucket()
    blob = bucket.blob(cloud_file_path)
    
    blob.upload_from_filename(local_file_path)

    # Optional: Make the file publicly accessible
    blob.make_public()

    # print(f"File uploaded to {blob.public_url}")


def get_latest_user():
    # Initialize Firestore client
    db = firestore.client()
    img_name = ""
    # Reference to the 'users' collection
    users_ref = db.collection('users').order_by("date", direction=firestore.Query.DESCENDING).limit(1).stream()
    # Query to order by a timestamp field in descending order
    # print(users_ref)
    for user in users_ref:

        # print(f"{user.to_dict()['name']}")
        # print(f"{user.to_dict()['email']}")
        
        # img_name =f"{user.id}_" +f"{user.to_dict()['name']}_"+ f"{user.to_dict()['email']}"
        img_name =f"{user.id}_" +f"{user.to_dict()['name']}_"

        # img_name = f"{user.id}"
        # print(f"{user.id}")
        # Execute the query
    return img_name
        
# Example usage
#latest_user = get_latest_user()
#if latest_user:
#    print(f"Latest user: {latest_user}")
#else:
#    print("No users found.")

name = 'new' #replace with your name

cam = PiCamera()
cam.resolution = (512, 304)
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))
    
img_counter = 0
img_path = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
# print("hold still...")

# for i in range (3, 0, -1):
#     print(i)
#     time.sleep(1)

img_name = get_latest_user()
cam.capture(img_path)
upload_to_storage(img_path, "images/{}.jpg".format(img_name))


print("captured!")
# print("{} written!".format(img_name))


