import cv2
import numpy as np
import pytesseract
#from .settings import rtsp

cam = cv2.VideoCapture(0)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    detector = cv2.FastFeatureDetector_create(threshold=50)
    while (True):
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = detector.detect(gray)
        i = 0
        while(i < len(result)):
            kp = result[i]
            cv2.circle(frame, (int(kp.pt[0]), int(kp.pt[1])), 10, (255, 0, 0, 255))
            i += 1

        cv2.imshow("frame", frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break