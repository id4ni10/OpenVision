import cv2
import numpy as np
import pytesseract
#from .settings import rtsp

cam = cv2.VideoCapture(0)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        biggestContourIdx = -1
        biggestContourArea = 0
        color = (255, 0, 0, 255)
        scalar = (255,255,255)
        i = 0

        while(i < len(contours)):
            cv2.drawContours(frame, contours, i, color, 1, 8, hierarchy, 0)

            ctArea = cv2.contourArea(contours[i])
            if(ctArea > biggestContourArea):
                biggestContourArea = ctArea
                biggestContourIdx = i

            i += 1

        boundingBox = cv2.minAreaRect(contours[biggestContourIdx])
        corners = cv2.boxPoints(boundingBox)
        corners = np.int0(corners)

        cv2.drawContours(frame, [corners], 0, scalar, 2)

        cv2.imshow("frame", frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break