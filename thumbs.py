import mediapipe
import cv2
from time import sleep
from cvzone.HandTrackingModule import HandDetector

camera = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8 , )

while True:
    success , img = camera.read()
    
    hand , img = detector.findHands(img)
    
    if hand :
        print(hand)
    
    cv2.imshow("a" , cv2.flip(img , 1))  
    
    sleep(2)
                
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break