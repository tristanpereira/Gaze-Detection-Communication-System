
import cv2
import numpy as np
import dlib
import time
import pyglet

bkgrd_path = r'C:\Users\100657242\Downloads\background.jpg'

cap = cv2.VideoCapture(0)
detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
th1 = 3
th2 = 3
th = 3

color1 = (0,0,255)
color2 = (0,0,255)

option = 1

bkgrd =  cv2.imread(bkgrd_path)

while True:
    _, frame = cap.read()
    flip = cv2.flip(frame,1)
    gray = cv2.cvtColor(flip, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    gui = np.zeros((1000,1500,3), np.uint8)
    x20=0
    y20=0
    width = 1500
    height = 1000

    cv2.rectangle(gui,(0,0),(750-th,1000-th),(0,0,255),th1)
    cv2.rectangle(gui,(750+th2,0),(1500,1000-th),(0,0,255),th2)

    #cv2.imshow('test',bkgrd)

    #bye = pyglet.media.load("bye.wav")

    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(flip, (x, y), (x1, y1), (0, 255, 0), 2)
        
        landmarks = predictor(gray,face)
       

        left_point = (landmarks.part(36).x, landmarks.part(36).y)
        right_point = (landmarks.part(39).x, landmarks.part(39).y)
        top_point = (int((landmarks.part(37).x + landmarks.part(38).x)/2) , int((landmarks.part(37).y + landmarks.part(38).y)/2))
        bottom_point = (int((landmarks.part(41).x + landmarks.part(40).x)/2) , int((landmarks.part(41).y + landmarks.part(40).y)/2))
        
        cv2.rectangle(gui,(0,0),(750-th1,1000-th1),color1,th1)
        cv2.rectangle(gui,(750+th2,0),(1500,1000-th2),color2,th2)

        if option == 1:
            cv2.putText(gui,'Greetings',(300,500),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
            cv2.putText(gui,'Farewells',(1050,500),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
        if option == 2:
            color1 = (0,0,255)
            color2 = (0,0,255)
            cv2.putText(gui,'Hi there',(300,500),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
            cv2.putText(gui,'Hi, one moment please',(1050,500),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
        if option == 3:
            color1 = (0,0,255)
            color2 = (0,0,255)
            cv2.putText(gui,'Thank You',(300,500),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
            cv2.putText(gui,'Bye',(1050,500),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)

        left_eye_region = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                            (landmarks.part(37).x, landmarks.part(37).y),
                            (landmarks.part(38).x, landmarks.part(38).y),
                            (landmarks.part(39).x, landmarks.part(39).y),
                            (landmarks.part(40).x, landmarks.part(40).y),
                            (landmarks.part(41).x, landmarks.part(41).y)], np.int32)
        height, width, _ = frame.shape
        mask = np.zeros((height, width), np.uint8)
        cv2.polylines(mask, [left_eye_region], True, 255, 2)
        cv2.fillPoly(mask, [left_eye_region], 255)
        left_eye = cv2.bitwise_and(gray, gray, mask=mask)

        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])
        gray_eye = left_eye[min_y: max_y, min_x: max_x]
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)

        threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
        eye = cv2.resize(gray_eye, None, fx=5, fy=5)
        #cv2.imshow("Eye", eye)

        cv2.imshow("Threshold", threshold_eye)
        #cv2.imshow("Left eye", left_eye)

        cv2.line(flip,top_point,bottom_point,(255, 0, 0), 1)
        cv2.line(flip, left_point, right_point, (255, 0, 0), 1)
        height, width = threshold_eye.shape

        left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
        left_side_white = cv2.countNonZero(left_side_threshold)
  
        right_side_threshold = threshold_eye[0: height, int(width / 2): width]
        right_side_white = cv2.countNonZero(right_side_threshold)+0.00001
        gaze_ratio = left_side_white / right_side_white

        cv2.putText(flip, str(gaze_ratio),(50,100),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),3)
        #cv2.putText(flip, str(right_side_white),(50,150),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),3)

        if gaze_ratio <= 0.6 :
            cv2.putText(flip, "Left",(50,150),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),3)
            th2=3
            color2 = (0,0,255)
            if th1 < 20:
                th1 = th1 + 1
            elif th1 >=20 and option == 1 :
                color1 =(0,255,0)
                time.sleep(0.5)
                th1 = 3
                option = 2
            elif th1 >=20 and option == 2 :
                
                color1 =(0,255,0)
                print ("Hi there")
                time.sleep(2)
                option = 1
                th1 = 3
                th2 = 3
            elif th1 >=20 and option == 3 :
                
                color1 =(0,255,0)
                print ("Thank you")
                time.sleep(2)
                option = 1
                th1 = 3
                th2 = 3
        elif gaze_ratio >= 1.5 :
            cv2.putText(flip, "Right",(50,150),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),3)
            th1=3
            color1 = (0,0,255)
            if th2 < 20:
                th2 =th2 + 1
            elif th2 >= 20 and option == 1:
                color2 =(0,255,0)
                time.sleep(0.5)
                th2 = 3
                option = 3
            elif th2 >= 20 and option == 2:
                
                color2 =(0,255,0)
                print ("One moment please")
                time.sleep(2)
                option = 1
                th1 = 3
                th2 = 3
            elif th2 >= 20 and option == 3:
                
                color2 =(0,255,0)
                print ("Bye")
              
                time.sleep(2)
                option = 1
                th1 = 3
                th2 = 3
        else :
            cv2.putText(flip, "Center",(50,150),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 0),3)
            th1=3
            th2=3            
    
    cv2.imshow("Frame", flip)
    cv2.imshow("GUI",gui)
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows() 