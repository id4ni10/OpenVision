import cv2
import numpy
import pytesseract
from settings import rtsp

cam = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)       
        
        cv2.imshow('gray', gray)
        
        text = pytesseract.image_to_string(gray)

        print(text)
    
        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break