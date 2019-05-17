import cv2
import numpy
url = "rtsp://71014217:123@10.10.10.209:8554/profile0"
#camera = cv2.VideoCapture("rtsp://admin:71014217:123@10.10.10.209:8554/xyz/video.smp")
cam = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
kernel = numpy.ones((5 ,5), numpy.uint8)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        rangomax = numpy.array([255, 50, 50]) # B, G, R
        rangomin = numpy.array([51, 0, 0])
        mask = cv2.inRange(frame, rangomin, rangomax)
        # reduce the noise
        opening = cv2.morphologyEx(mask, cv2.MORPH_BLACKHAT, kernel)

        x, y, w, h = cv2.boundingRect(opening)

        cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)
    
        cv2.imshow('camera', frame)
    
        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break