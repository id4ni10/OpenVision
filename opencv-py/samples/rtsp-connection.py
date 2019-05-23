import cv2
from .settings import rtsp

cam = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        cv2.imshow('contornos', frame)
        
        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break