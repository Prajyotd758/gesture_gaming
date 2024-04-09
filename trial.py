import mediapipe as mp
import numpy as np
import cv2
from pynput.keyboard import Key , Controller
from time import sleep
import math

myKeyboard = Controller()
camera = cv2.VideoCapture(0)
hands = mp.solutions.hands
controller = hands.Hands(static_image_mode = False, max_num_hands = 2 , min_detection_confidence = 0.7 )
draw = mp.solutions.drawing_utils

from pynput import keyboard

pressed = {}

def on_press(key): 
    if key not in pressed: # Key was never pressed before
        pressed[key] = False
    
    if not pressed[key]: # Same logic
        pressed[key] = True
        # print('Key %s pressed' % key) 
        
def on_release(key):  # Same logic
    if pressed[key]:
        pressed[key] = False
        # print('Key %s released' %key)
        
with keyboard.Listener( on_press=on_press, on_release=on_release) as listener: 
    
    while camera.isOpened():
        success , img = camera.read()
        
        if not success or img is None:
            continue
        
        img.flags.writeable = True
        rgb = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        x, y, c = img.shape
        
        op = controller.process(rgb)
        co = []
        if op.multi_hand_landmarks:
            for i in op.multi_hand_landmarks:
                draw.draw_landmarks(img , i , hands.HAND_CONNECTIONS)
                for lm in i.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    co.append([lmx, lmy])
                
                
        if len(co) == 42:             
            x1 , y1 ,x2 , y2 = co[12][0] , co[12][1] ,co[33][0] , co[33][1]
            x3 , y3 ,x4, y4   = co[4][0] , co[4][1],co[25][0] , co[25][1]
            length =int(math.hypot(x2 - x1, y2 - y1))
            length_thumb = int(math.hypot(x4 - x3, y4 - y3))
            
            percetage = int((60*length)//100)
                       
            if(co[0][0] > co[12][0] and co[0][0] < co[12][1]):
                print("right")
                myKeyboard.press(Key.right)
                            
            elif((co[29][0] > co[29][1] and co[33][0] > co[33][1]) and (co[37][0] < co[37][1] and co[41][0] < co[41][1])):
                print("nitro")
                myKeyboard.press(Key.alt)
                
            elif (length_thumb > percetage):
                print("Left")
                myKeyboard.press(Key.left)
                
            elif (co[28][1] < co[21][1] and  co[28][1] > co[26][1]):
                print("down")
                myKeyboard.release(Key.left)
                myKeyboard.release(Key.alt)
                myKeyboard.release(Key.right)
                myKeyboard.release(Key.up)
                myKeyboard.press(Key.down)
                 
            elif (co[41][0] > co[41][1]):
                print("up")
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
        
        # sleep(0.5)
        
        
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break
        
        
camera.release()
        