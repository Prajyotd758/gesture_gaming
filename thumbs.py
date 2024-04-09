import cv2
from time import sleep
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key , Controller
from pynput import keyboard

camera = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8 ,)
myKeyboard = Controller()

pressed = {}

def on_press(key): 
    if key not in pressed: # Key was never pressed before
        pressed[key] = False
    
    if not pressed[key]: 
        pressed[key] = True
        # print('Key %s pressed' % key) 
        
def on_release(key):  # Same logic
    if pressed[key]:
        pressed[key] = False
        # print('Key %s released' %key)
        

with keyboard.Listener( on_press=on_press, on_release=on_release) as listener:
    while camera.isOpened():
        success , img = camera.read()
        hand , img = detector.findHands(img)
        
        if len(hand) == 2 :
            
            fingers = detector.fingersUp(hand[1])
            
            # nitroo
            if ((fingers[3] == 0 and fingers[4] == 0) and (fingers[1] == 1 and fingers[2] == 1)): 
                print("nitro")
                myKeyboard.press(Key.alt)
            
            # down key    
            elif all(v == 0 for v in fingers):
                print("down")
                myKeyboard.release(Key.left)
                myKeyboard.release(Key.alt)
                myKeyboard.release(Key.right)
                myKeyboard.release(Key.up)
                myKeyboard.press(Key.down)
                
            # right key    
            elif((hand[0]['lmList'][0][0] > hand[0]['lmList'][12][0] )and (hand[0]['lmList'][0][0] > hand[0]['lmList'][12][1])):
                print("right")
                myKeyboard.press(Key.right)
                
            # left key    
            elif((hand[0]['lmList'][0][0] < hand[0]['lmList'][12][1]) and (hand[0]['lmList'][0][0] < hand[0]['lmList'][12][0] ) ):
                print("left")
                myKeyboard.press(Key.left)
                
            # up key    
            else:
                print("forward")
                myKeyboard.release(Key.alt)
                myKeyboard.release(Key.left)
                myKeyboard.release(Key.right)
                myKeyboard.release(Key.down)
                myKeyboard.press(Key.up)
        
        else:
            myKeyboard.release(Key.down)
            myKeyboard.release(Key.up)
            myKeyboard.release(Key.alt)
            myKeyboard.release(Key.right)
            myKeyboard.release(Key.left)   
        
        cv2.imshow("a" , cv2.flip(img , 1))  
                        
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break
    
camera.release()