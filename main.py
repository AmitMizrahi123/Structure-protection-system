import cv2
import face_recognition
from server import db_collection, fs
import numpy as np


images_list = []
names_list = []
encoding_list = []

for images in db_collection.find():
    name = images['username']
    image = images['images'][0]
    g_out = fs.get(images['images'][0]['imageID'])
    img = np.frombuffer(g_out.read(), dtype=np.uint8)
    img = np.reshape(img, image['shape'])
    images_list.append(img)
    names_list.append(name)
    encode = face_recognition.face_encodings(img)[0]
    encoding_list.append(encode)


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    image_location = face_recognition.face_locations(img)
    image_encoding = face_recognition.face_encodings(img, image_location)

    for encode_face, location_face in zip(image_encoding, image_location):
        matches = face_recognition.compare_faces(encoding_list, encode_face)

        name = "Unknown Person"
        color = (0, 0, 255)
        text_color = (0, 0, 0)

        if True in matches:
            first_match_index = matches.index(True)
            name = names_list[first_match_index]
            color = (0, 255, 0)

        top, right, bottom, left = location_face
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)
        cv2.rectangle(img, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_PLAIN, 1.3, text_color, 2)

    cv2.imshow('iamge', img)
    cv2.waitKey(1)