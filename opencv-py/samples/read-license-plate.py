import re
import cv2
import numpy as np
import pytesseract
import threading
from settings import rtsp

plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

cam = cv2.VideoCapture(rtsp)
cam.set(3, 136)
cam.set(4, 96)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = plate_cascade.detectMultiScale(gray, 1.3, 5)
        crop = None
        for (x, y, w, h) in faces:
            crop = gray[y : y + h, x : x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
            if crop.any():
                cv2.imshow('ocr', crop)

                thresh, bw = cv2.threshold(crop, 225, 255, cv2.THRESH_OTSU | cv2.THRESH_TOZERO)
                cv2.imshow('bw', bw)

                text = pytesseract.image_to_string(bw, lang='por', config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                plate = re.search('\w{3}\d{1}\w{1}\d{2}', text)

                if(plate):
                    print(plate)
                else:
                    print(text)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break