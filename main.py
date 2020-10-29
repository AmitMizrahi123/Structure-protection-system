import cv2
import face_recognition
from server import db_collection, fs
import numpy as np
from message import send_message


flag = True
images_list = []
names_list = []
phone_list = []
encoding_list = []

for images in db_collection.find():
    name = images['username']
    phone_number = images['phone_number'].replace('0', '+972', 1)  # Replace the number to israel number
    image = images['images'][0]
    g_out = fs.get(image['imageID'])
    img = np.frombuffer(g_out.read(), dtype=np.uint8)
    img = np.reshape(img, image['shape'])
    images_list.append(img)
    names_list.append(name)
    phone_list.append(phone_number)
    encode = face_recognition.face_encodings(img)[0]
    encoding_list.append(encode)

video_capture = cv2.VideoCapture(0)

while True:
    success, frame = video_capture.read()
    image_location = face_recognition.face_locations(frame)
    image_encoding = face_recognition.face_encodings(frame, image_location)

    name = "Unknown Person"
    color = (0, 0, 255)
    text_color = (0, 0, 0)

    for encode_face, location_face in zip(image_encoding, image_location):
        matches = face_recognition.compare_faces(encoding_list, encode_face)

        if True in matches:
            first_match_index = matches.index(True)
            name = names_list[first_match_index]
            color = (0, 255, 0)
            flag = True

        top, right, bottom, left = location_face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_PLAIN, 1.2, text_color, 2)

    cv2.imshow('iamge', frame)

    if flag and name == "Unknown Person":
        send_message(phone_list)
        flag = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
