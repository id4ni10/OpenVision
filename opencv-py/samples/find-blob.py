import cv2
import numpy
import pytesseract
from settings import rtsp

def find_blobs(img):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
     
    # Change thresholds
    params.minThreshold = 100
    params.maxThreshold = 5000
     
    # Filter by Area.
    params.filterByArea = True
    #params.minArea = 200
    #params.maxArea = 200
     
    # Filter by Circularity
    params.filterByCircularity = True
    #params.minCircularity = 1
     
    # Filter by Convexity
    params.filterByConvexity = True
    #params.minConvexity = 1
     
    # Filter by Inertia
    #params.filterByInertia = True
    #params.minInertiaRatio = 0.01

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)
     
    # blobs Detectados.
    keypoints = detector.detect(img)
      
    # Desenhar os keypoints com circulos vermelhos.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS desenha exatamente o tamanho do circulo encontrado
    im_with_keypoints = cv2.drawKeypoints(img, keypoints, numpy.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,)
    #cv2.drawContours(img, im_with_keypoints, -1, (0, 255, 0), 2)
    print (keypoints)
    for k in keypoints:
        x = int(k.pt[0])
        y = int(k.pt[1])
        pos = str(k.pt)
        cv2.putText(im_with_keypoints,pos , (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 2, cv2.LINE_AA)

    cv2.imshow("blobs", im_with_keypoints)

cam = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        find_blobs(frame)
    
        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break