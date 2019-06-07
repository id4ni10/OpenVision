import cv2
import numpy as np
import pytesseract
from settings import rtsp

cam = cv2.VideoCapture(rtsp)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    params = cv2.SimpleBlobDetector_Params()

    params.filterByCircularity = True

    #params.minThreshold = 450
    #params.maxThreshold = 500

    #params.filterByArea = True
    #params.minArea = 200
    #params.maxArea = 200

    detector = cv2.SimpleBlobDetector_create(params)
    red = (255, 0, 0, 255)
    green = (0, 255, 0)

    while (True):
        ret, frame = cam.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        keypoints = detector.detect(gray)
        i = 0
        while(i < len(keypoints)):
            kp = keypoints[i]
            cv2.circle(frame, (int(kp.pt[0]), int(kp.pt[1])), 10, green if len(keypoints) == 4 else red)
            i += 1

        cv2.imshow("frame", frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break