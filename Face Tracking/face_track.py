import sys
sys.path.append("/home/jetbot/jetbot")
import numpy as np
import cv2
from jetbot.robot import Robot
import time

robot = Robot()

#robot.left(0.3)
#time.sleep(0.5)
#robot.stop()

USB = False
no_face = 0
if USB:
    camera= cv2.VideoCapture(0)
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
		if len(results) == 0:
		    no_face +=1
		if no_face > 100:
			no_face = 0
		if no_face > 10:
		    robot.stop()
		for (x,y,w,h) in results:
		    no_face = 0
		    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		    #print(w)
		    if w < 180:
			    robot.set_motors(0.1, 0.1)
		    elif w >= 180:
			    robot.stop()
		    else:
			    robot.stop()
		cv2.imshow("test", img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break
		#print(no_face)
except KeyboardInterrupt:
	pass
finally:
	robot.stop()
	camera.release()
	cv2.destroyAllWindows()

