import re
import cv2
import numpy as np
import pytesseract
import threading
from settings import rtsp
from datetime import datetime

plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

cam = cv2.VideoCapture(0)
#cam.set(3, 91)
#cam.set(4, 64)

def fix_cap(capture):
    find = str(capture.group(0))

    if(re.search('[UQOD]', find[3])):
        return '{start}0{end}'.format(start = find[0:3], end = find[4:7])

    return find

def tesseract_read(capture):
    return pytesseract.image_to_string(capture, lang='por', config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def read_text(capture):
    text = tesseract_read(capture)

    plate_success = re.search('\w{3}\d{1}\w{1}\d{2}', text)
    plate_fix_cap = re.search('\w{3}\w{1}\w{1}\d{2}', text)

    if(plate_success):
        return True, plate_success.group(0)
    elif(plate_fix_cap):
        return True, fix_cap(plate_fix_cap)
    return False, text

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = plate_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            crop = gray[y : y + h, x : x + w]
            cv2.imshow('crop', crop)
            if crop.any():
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                thresh, bw = cv2.threshold(crop, 225, 255, cv2.THRESH_OTSU | cv2.THRESH_TOZERO)
                cv2.imshow('bw', bw)
                result, text = read_text(bw)

                if(result):
                    print('{text} - {now}'.format(text = text, now = datetime.today()))

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break