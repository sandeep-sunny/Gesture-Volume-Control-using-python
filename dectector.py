from myhand import HandDetector
import cv2
import math
import numpy as np
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pyca.pycaw import AudioUtilies,IAudioEndpointVolume

handDetector=HandDetector(min_detecion_confidence=0.7)
webcamFeed=cv2.VideoCapture(0)

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
while True:
    status,image=webcamFeed.read()
    handLandmarks=handDetector.findHandLandMarks(image=image,draw=True)
  
    if(len(handLandmarks) !=0):

        x1,y1=handLandmarks[4][1],handLandmarks[4][2]
        x2,y2=handLandmarks[0][1],handLandmarks[0][2]
        length=math.hypot(x2-x1,y2-y1)
        print(length)
        volumeValue=np.interp(length,[50,250],[-65.25,0.0])
        volume.setMasterVolumeLevel(volumeValue,None)

        cv2.circle(image,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(image,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(image,(x1,y1),(x2,y2),(255,0,255),3)

    cv2.imshow("Volume",image)
    cv2.waitKey(1)
    
