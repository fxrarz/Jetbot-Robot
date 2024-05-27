import numpy as np
import cv2
import time


USB = True
if USB:
    camera= cv2.VideoCapture(0)
    print("USB or Webcam accepted")
    
else:
    camera_pipeline = "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),\
    width=640, height=480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, \
    width=(int)640, height=(int)480, format=(string)BGRx ! videoconvert ! appsink"
    camera = cv2.VideoCapture(camera_pipeline, cv2.CAP_GSTREAMER)

#---loading the Haar Cascade detector using CascadeClassifier---
face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
try:
	while 1:
		#---Loading the image from camera -----
		_, img = camera.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		results = face_detector.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in results:
		    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		    print(w)
		cv2.imshow("test", img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break
except KeyboardInterrupt:
	pass
finally:
	camera.release()
	cv2.destroyAllWindows()

