import cv2
import numpy
import pytesseract
import threading
from settings import rtsp

plate_cascade = cv2.CascadeClassifier('opencv-py\samples\haarcascade_russian_plate_number.xml')
cam = cv2.VideoCapture(rtsp)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        
        faces = plate_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop = gray[y : y + h, x : x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('ocr', crop)
            print(pytesseract.image_to_string(crop, lang='por'))

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break