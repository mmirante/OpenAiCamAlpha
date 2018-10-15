import cv2
import urllib 
import numpy as np
from time import sleep

count = 0
files = "img"
filee = ".jpg"
filename = ""

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
StreamIP='192.168.0.20'
StreamPort=8080

stream=urllib.urlopen('http://' + StreamIP + ':' + StreamPort + '/?action=stream')
face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_smile.xml')
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) != 0:
          count = count + 1
          filename = files + str(count) + filee
          print "Faces detected:", filename
          cv2.imwrite(filename, i)
          #out.write(i)
        else:
          print "Faces NOT detected"

	for (x,y,w,h) in faces:
	   cv2.rectangle(i,(x,y),(x+w,y+h),(255,0,0),2)
           roi_gray = gray[y:y+h, x:x+w]
	   roi_color = i[y:y+h, x:x+w]
        #   eyes = eye_cascade.detectMultiScale(roi_gray)
        #   for (ex,ey,ew,eh) in eyes:
        #       cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
          # for (ex,ey,ew,eh) in eyes:
          #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        sleep(0.5)	
        #cv2.imshow('i',i)
        if cv2.waitKey(1) ==27:
            #out.release()
            #cv2.destroyAllWindows()
            exit(0)   
