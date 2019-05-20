import cv2
import numpy
#url = "rtsp://71014217:123@10.10.10.209:8554/profile0"

#cam = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
cam = cv2.VideoCapture(0)
kernel = numpy.ones((5 ,5), numpy.uint8)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, imagembin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
        imagemdesfoq = cv2.GaussianBlur(imagembin, (5,5), 0)
        contornos, hier = cv2.findContours(imagemdesfoq, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2)
        #circles = cv2.HoughCircles(imagemdesfoq, cv2.HOUGH_GRADIENT, 1.2, 100)
        for c in contornos:
            contornofechado = cv2.arcLength(c, True)
            aproximarforma = cv2.approxPolyDP(c, 0.03 * contornofechado, True)
            cv2.imshow('contornos', frame)

            #rangomax = numpy.array([255, 50, 50]) # B, G, R
            #rangomin = numpy.array([51, 0, 0])
           # mask = cv2.inRange(frame, rangomin, rangomax)
        # reduce the noise
            #opening = cv2.morphologyEx(mask, cv2.MORPH_BLACKHAT, kernel)

            #x, y, w, h = cv2.boundingRect(opening)

            #cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
            #cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)
    
        #cv2.imshow('camera', frame)
        #cv2.imshow('cinza', cinza)
        #cv2.imshow('Binarizada', imagembin)
        #cv2.imshow('Sem Ruidos + Desfoque', imagemdesfoq)
    
        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break