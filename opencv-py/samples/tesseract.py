import cv2
import numpy
import pytesseract
import threading
from settings import rtsp

cam = cv2.VideoCapture(rtsp)

def run_ocr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    retval, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    #th3 = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    print(pytesseract.image_to_string(threshold, lang='por'))

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        #retval, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        print(pytesseract.image_to_string(th3, lang='por'))

        cv2.imshow('frame', th3)

        #thread1 = threading.Thread(target=run_ocr, args=(frame,))

        #thread1.start()

        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break