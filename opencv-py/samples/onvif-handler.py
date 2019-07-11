from settings import host, port, username, password
from onvif import ONVIFCamera

cam = ONVIFCamera(host, port, username, password, '/etc/onvif/wsdl/')

if cam is None: #or not cam.isOpened():
    print('Warning: unable to open video source: ', cam)
else:
    while (True):
        print(cam)
        break