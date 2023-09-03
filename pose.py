import cv2
import math
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
msg=""
def findAngle(lmList,img, p1, p2, p3):
        
        x1, y1 = lmList[p1][1:3]
        x2, y2 = lmList[p2][1:3]
        x3, y3 = lmList[p3][1:3]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        return angle
def WarriorPose(img,lmList):
    if(165<=findAngle(lmList,img,11,13,15)<=195 and 165<=findAngle(lmList,img,12,14,16)<=195 ):
        if(165<=findAngle(lmList,img,24,26,28)<=195 or 165<=findAngle(lmList,img,23,25,27)<=195):
            if(200<=findAngle(lmList,img,24,26,28)<=250 or 200<=findAngle(lmList,img,23,25,27)<=250):
                return True
    return False
        
def TreePose(img,lmList):
    if(165<=findAngle(lmList,img,24,26,28)<=195 or 165<=findAngle(lmList,img,23,25,27)<=195):
        if(315<=findAngle(lmList,img,24,26,28)<=335 or 315<=findAngle(lmList,img,23,25,27)<=335):
            return True  
    return False
def TPose(img,lmList):
    
    if(200<=findAngle(lmList,img,24,26,28)<=250 and 150<=findAngle(lmList,img,23,25,27)<=195):
         if(165<=findAngle(lmList,img,11,13,15)<=195 or 165<=findAngle(lmList,img,12,14,16)<=195 ):
                return True
    return False

def capture(ch):
    try:
        global msg
        ch=int(ch)
        l=["Tree Pose Yoga","T Pose Yoga","Warrior Pose Yoga","Biceps Curl Workout","Push Ups Workout"]
        path="Images/"+str(ch)+".mp4"
        cap=cv2.VideoCapture(path)
        detector=PoseDetector()
        counter=-1
        count=0
        dir=0
        displayText="Invalid Pose"
        while True:
            success,img=cap.read()
            if success:
                img=cv2.resize(img,(1280,720))
                imgDraw = detector.findPose(img)
                lmlist,_=detector.findPosition(img)
                if len(lmlist)!=0:
                    if(ch==1):
                        if TreePose(img,lmlist):
                            if(counter==-1):
                                counter=0
                            else:
                                counter+=1
                    elif(ch==2):
                        if TPose(img,lmlist):
                            if(counter==-1):
                                counter=0
                            else:
                                counter+=1
                    elif(ch==3):
                        if WarriorPose(img,lmlist):
                            if(counter==-1):
                                counter=0
                            else:
                                counter+=1
                    elif(ch==4):
                        per=np.interp(findAngle(lmlist,img,11,13,15),(120,340),(0,100))
                        if(per==100 and dir==0):
                            count+=0.5
                            dir=1
                        elif(per==0 and dir==1):
                            count+=0.5
                            dir=0

                    elif(ch==5):
                        per=np.interp(int(findAngle(lmlist,img,11,13,15)),(200,270),(0,100))
                        if(per==100 and dir==0):
                            count+=0.5
                            dir=1
                        elif(per==0 and dir==1):
                            count+=0.5
                            dir=0
                    if(ch==1 or ch==2 or ch==3):
                        if(counter==-1):
                            displayText="Invalid Pose"
                        else:
                            displayText="No of seconds="+str(counter//60)
                    if(ch==4 or ch==5):
                            displayText="No of Times="+str(int(count))
                    cvzone.putTextRect(img,displayText,(50,50))
                    ret,buffer=cv2.imencode('.jpg',img)
                    if ret:
                        img=buffer.tobytes()
                        yield(b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+img+b'\r\n')      
            else:
                msg="Today's wokout pose is "+l[ch-1]+"."+displayText+"."
                break
        
    except:
        print("Error")