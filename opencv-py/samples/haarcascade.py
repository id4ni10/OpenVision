import numpy as np
import cv2

tank_cascade = cv2.CascadeClassifier('opencv-py\samples\haarcascade_tank.xml')
cam = cv2.VideoCapture(0)

#gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = tank_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break


