import cv2
import numpy
from PIL import Image
import pytesseract

def find_blobs(img, gray):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
     
    # Change thresholds
    params.minThreshold = 40
    params.maxThreshold = 100
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 170
    params.maxArea = 185
     
    params.blobColor = 0    
    
    # Filter by Circularity
    #params.filterByCircularity = True
    #params.minCircularity = 0.8
     
    # Filter by Convexity
    params.filterByConvexity = False
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
    #print (keypoints)
    contours = []
    crop = gray
    
    for k in keypoints:
        x = int(k.pt[0])
        y = int(k.pt[1])
        pos = str(k.pt)
        cv2.putText(im_with_keypoints, pos , (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 2, cv2.LINE_AA)
        contours.append(numpy.array([x, y], dtype=numpy.int32))

    if len(contours) == 4:        
        # find min and max
        print(numpy.sort(contours, order= numpy.min(contours)))
       # print(contours)
        #crop = im_with_keypoints[y : contours[0], x :  contours[3]]
        #cv2.imshow("cinza", crop)

    #min = im_with_keypoints[0]
    #max = im_with_keypoints[3]

    #print(min.pt[0])
    #print(min.pt[1])
    #print(contours)

    #cv2.drawContours(im_with_keypoints, contours, -1, (0, 255, 0), 2, 8, hierarchy, 0)

    cv2.imshow("blobs", im_with_keypoints)         

#url = "rtsp://71014217:123@10.10.10.205:8554/profile0"
#cam = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
cam = cv2.VideoCapture(0)
kernel = numpy.ones((5 ,5), numpy.uint8)

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        ret, frame = cam.read()
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #text = pytesseract.image_to_string(cinza)
        #print(text)
        
        find_blobs(frame, cinza)
    
        #cv2.imshow('camera', frame)
        #cv2.imshow('cinza', cinza)
        #cv2.imshow('Binarizada', imagembin)
        #cv2.imshow('Sem Ruidos + Desfoque', imagemdesfoq)
    
        k = cv2.waitKey(1) & 0xFF
    
        if k == 27:
            break



        #Comentarios

        #_, imagembin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
        #imagemdesfoq = cv2.GaussianBlur(imagembin, (5,5), 0)
        #contornos, hier = cv2.findContours(imagemdesfoq, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2)
        #circles = cv2.HoughCircles(imagemdesfoq, cv2.HOUGH_GRADIENT, 1.2, 100)
        #for c in contornos:
            #contornofechado = cv2.arcLength(c, True)
            #aproximarforma = cv2.approxPolyDP(c, 0.03 * contornofechado, True)
            #cv2.imshow('contornos', frame)

            #rangomax = numpy.array([255, 50, 50]) # B, G, R
            #rangomin = numpy.array([51, 0, 0])
            #mask = cv2.inRange(frame, rangomin, rangomax)
            # reduce the noise
            #opening = cv2.morphologyEx(mask, cv2.MORPH_BLACKHAT, kernel)

            #x, y, w, h = cv2.boundingRect(opening)

            #cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 3)
            #cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)
