import numpy as np
import cv2

from settings import rtsp

cam = cv2.VideoCapture(rtsp)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,127,255,1)

        contours,h = cv2.findContours(thresh,1,2)

        for contour in contours:
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
                        
            area = cv2.contourArea(contour)
            if ((len(approx) == 4)):
                (x, y, w, h) = cv2.boundingRect(approx)
                if  ((float(w)/h)==1):
                    cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 2)
                else:
                    cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 2)

                #contour_list.append(contour)    
        
        cv2.imshow('frame', img)
        
        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break