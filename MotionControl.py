import win32gui; import cv2; import mediapipe as mp; import numpy; import win32api, win32con; import ctypes; import time
from mediapipe.python.solutions import hands_connections; from mediapipe.python.solutions.drawing_utils import DrawingSpec
from mediapipe.python.solutions.hands import HandLandmark; import random; import math; import numpy; import mouse; import keyboard
 
def Prompts():
  global CursorControl
  # CursorControl = input('Do you want to control the cursor with motion? (y/n) \n')
  CursorControl = 'y'
  if CursorControl == 'y':
    CursorControl = True
  else:
    print('No cursor control.')
    CursorControl = False
 
#MK Motion Control
def main():
  global mp_drawing; global mp_drawing_styles; global mp_pose
  Prompts()
 
  #SET MEDIAPIPE UTILITIES/STYLES/HAND STUFF
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_hands = mp.solutions.hands
  # mp_pose = mp.solutions.pose
 
  #INITIALIZE VARIABLES
  HandCounter = 0; LostHandCount = 0; ActiveHandCount = 0;xTotal = 0; yTotal = 0; xCoord = 0; yCoord = 0
  LastxCoordwrist = 0; LastyCoordwrist = 0; LeftClickDown = False; UpCount = 0; DownCount = 0
  INDEXDOWN = False; MIDDLEDOWN = False; RINGDOWN = False; PINKYDOWN = False; HandShown = False
  MouseSensitivity = 5; ImageSizeMod = 5
 
  #INITIALIZE ARRAYS
  xlinearray = []; ylinearray = []; Rarray = []; Garray = []; Barray = []; xCoordarray = []; yCoordarray = []
 
  #GET SCREEN DIMENSIONS
  user32 = ctypes.windll.user32; ScreenWidth = user32.GetSystemMetrics(0); ScreenHeight = user32.GetSystemMetrics(1)
 
  #START CAMERA
  global cap; global image; global CursorControl
  cap = cv2.VideoCapture(0) 
  with mp_hands.Hands(
      model_complexity=1,
      min_detection_confidence=0.8,
      min_tracking_confidence=0.3) as hands:
    #WHILE CAMERA IS OPEN
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        continue
  
      if cv2.waitKey(1) & 0xFF == ord('c'):
        CursorControl = True
      elif cv2.waitKey(1) & 0xFF == ord('x'):
        CursorControl = False
      
      #MARKING IMAGE AS NON-WRITABLE IMPROVES PERFORMANCE
      image.flags.writeable = False
      
      #BGR TO RGB
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      
      #SET ALL HAND-RELATED VARIABLES UNDER 'results'
      results = hands.process(image)
 
      #REVERT IMAGE TO OG FORM AND CONSIDER DRAWING A HAND
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      CheckTimer = time.time
      
      #IF AT LEAST ONE HAND IS FOUND
      if results.multi_hand_landmarks:
        LostHandCount = 0; ActiveHandCount += 1; HandShown = True
        for i in results.multi_handedness:
          #DETERMINE IF RIGHT/LEFT HAND ARE SHOWN
          LeftHand = False
          if str(i.classification[0].label) == 'Right':
            LeftHand = True
          RightHand = False
          if str(i.classification[0].label) == 'Left':
            RightHand = True
 
        #LOOP ACROSS EVERY FINGER LANDMARK/CONNECTION IN THIS FRAME, DO PLENTY OF MATH
        for hand_landmarks in results.multi_hand_landmarks:
          imageX = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
          imageY = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
          image_height, image_width, _ = image.shape
                  
          #INDEX FINGER TIP
          xCoordindex = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * ScreenWidth))
          yCoordindex = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * ScreenHeight)
 
          #INDEX FINGER MIDDLE KNUCKLE
          xCoordindexmidknuckle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * ScreenWidth))
          yCoordindexmidknuckle = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * ScreenHeight)
          
          #INDEX FINGER UPPER KNUCKLE
          xCoordindexupperknuckle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x * ScreenWidth))
          yCoordindexuppernuckle = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * ScreenHeight)
          
          #INDEX FINGER KNUCKLE
          xCoordindexknuckle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * ScreenWidth))
          yCoordindexknuckle = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * ScreenHeight)
          
          #MIDDLE FINGER TIP
          xCoordmiddle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * ScreenWidth))
          yCoordmiddle = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * ScreenHeight)
          xRealimagemiddle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
          yRealimagemiddle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
          
          #MIDDLE FINGER KNUCKLE
          xCoordmiddleknuckle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * ScreenWidth))
          yCoordmiddleknuckle = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * ScreenHeight)
          xRealimagemiddleknuckle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
          yRealimagemiddleknuckle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
          xAnimation = int(xRealimagemiddleknuckle*image_width)
          yAnimation = int(yRealimagemiddleknuckle*image_height)
          
          #RING FINGER TIP
          xCoordring = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * ScreenWidth))
          yCoordring = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * ScreenHeight)
          
          #RING FINGER KNUCKLE
          xCoordringknuckle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * ScreenWidth))
          yCoordringknuckle = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * ScreenHeight)
          
          #PINKY TIP
          xCoordpinky = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * ScreenWidth))
          yCoordpinky = int((hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * ScreenHeight))
          xRealimagepinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
          yRealimagepinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y 
          
          #PINKY KNUCKLE
          xCoordpinkyknuckle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x * ScreenWidth))
          yCoordpinkyknuckle = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * ScreenHeight)
          
          #THUMB TIP
          xCoordthumb = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * ScreenWidth))
          yCoordthumb = int((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * ScreenHeight))
          xRealimagethumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
          yRealimagethumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
          
          #THUMB KNUCKLE
          xCoordthumbknuckle = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x * ScreenWidth))
          yCoordthumbknuckle = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * ScreenHeight)
          
          #WRIST
          xCoordwrist = int(ScreenWidth - (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * ScreenWidth))
          yCoordwrist = int((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * ScreenHeight))
          xRealimagewrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x 
          yRealimagewrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
          
          #DIV/0 HANDLER
          if xCoord == 0:
            xCoord = 1
          if yCoord == 0:
            yCoord = 1
          if xCoordwrist == 0:
            xCoordwrist = 1
          if yCoordwrist == 0:
            yCoordwrist = 1
          
          #DETERMINE WHICH FINGER TIPS ARE BENT BELOW THE KNUCKLE
          if yCoordindexknuckle <= yCoordindex and yCoordindex < yCoordwrist:
            INDEXDOWN = True
          else:
            INDEXDOWN = False
          if yCoordmiddleknuckle <= yCoordmiddle and yCoordmiddle < yCoordwrist:
            MIDDLEDOWN = True
          else:
            MIDDLEDOWN = False
          if yCoordringknuckle <= yCoordring and yCoordring < yCoordwrist:
            RINGDOWN = True
          else:
            RINGDOWN = False
          if yCoordpinkyknuckle <= yCoordpinky and yCoordpinky < yCoordwrist:
            PINKYDOWN = True
          else:
            PINKYDOWN = False     
                     
          #IF X IS FAR TO THE LEFT OR RIGHT, SET CURSOR ALONG LEFT/RIGHT EDGE
          if xCoordmiddle >= int(0.99*ScreenWidth):
            xCoordmiddle = int(0.99*ScreenWidth)
          elif xCoordmiddle <= int(0.01*ScreenWidth):
            xCoordmiddle = int(0.01*ScreenWidth)
          
          #IF Y IS FAR TO THE TOP OR BOTTOM, SET CURSOR ALONG TOP/BOTTOM EDGE
          if yCoordmiddle >= int(0.98*ScreenHeight) and int(0.98*ScreenHeight) > 0:
            yCoordmiddle = int(0.97*ScreenHeight)
          elif yCoordmiddle <= int(0.02*ScreenHeight):
            yCoordmiddle = int(0.02*ScreenHeight)
 
          #DISTANCE BETWEEN 2 POINTS FORMULA FOR WIDTH AND HEIGHT      
          HandWidth = int(math.sqrt((((xRealimagethumb-xRealimagepinky)**2)*image_width*280)+((yRealimagethumb-yRealimagepinky)**2)*image_height*280))
          HandHeight = int(math.sqrt((((xRealimagemiddle-xRealimagemiddleknuckle)**2)*image_width*900)+((yRealimagemiddle-yRealimagemiddleknuckle)**2)*image_height*900))
          if HandWidth <= 0:
            HandWidth = 1
          if HandHeight <= 0:
            HandHeight = 1
            
          DistanceFromScreen = int(image_height/HandHeight)
          
          if int(DistanceFromScreen) < 6:
            DistanceFromScreen = 6
          
          #PERCENT DIFFERENCE BETWEEN CURRENT CURSOR AND LAST CURSOR/CURRENT WRIST AND LAST WRIST
          xDiff = abs((xCoord-xCoordmiddle)/xCoord)*100; yDiff = abs((yCoord-yCoordmiddle)/yCoord)*100
          xDiffwrist = abs((xCoordwrist-LastxCoordwrist)/xCoordwrist)*100; yDiffwrist = abs((yCoordwrist-LastyCoordwrist)/yCoordwrist)*100
 
          #IF PERCENT DIFFERENCE OF RING FINGER IS HIGH, MOVE CURSOR WITH 10x MOTION BUFFER
          if (xDiff >= 0.4 or yDiff >= 0.4) and HandCounter >= 60 and CursorControl == True:
            xCoordarray.insert(0,xCoordmiddle)
            yCoordarray.insert(0,yCoordmiddle)
            if len(xCoordarray) >= int(DistanceFromScreen/1.5):
              xCoordarray = xCoordarray[0:int(DistanceFromScreen/1.5)]
              yCoordarray = yCoordarray[0:int(DistanceFromScreen/1.5)]
            xTotal = 0
            yTotal = 0
            for i in range(len(xCoordarray)):
              xTotal = xTotal + xCoordarray[i]
              yTotal = yTotal + yCoordarray[i]
            #SET COORDINATES TO THE MOVING AVERAGE OF THE PREVIOUS 'X' NUMBER OF CURSOR POSITIONS
            xCoord = int(xTotal/len(xCoordarray))
            yCoord = int(yTotal/len(xCoordarray))
            #IF COORDINATE ARRAY IS LONGER THAN SENSITIVITY THRESHOLD, POP OFF OLDEST ELEMENT
            if len(xCoordarray) >= DistanceFromScreen/1.5:
                xCoordarray.pop(int((DistanceFromScreen-1)/1.5))
                yCoordarray.pop(int((DistanceFromScreen-1)/1.5))
            #SET CURSOR POSITIONS
            win32api.SetCursorPos((int(xCoord),int(yCoord)))
 
          #ARCTANGENT OF MIDDLE FINGER HEIGHT TO WRIST CENTER
          RotationAngle = math.degrees(numpy.arctan((yRealimagemiddle-yRealimagewrist)/(xRealimagemiddle-xRealimagewrist)))+90
          
          #IF HAND IS IN FRAME LONG ENOUGH, ACTIVATE CURSOR CONTROLS
          if HandCounter >= 60:
            # if len(results.multi_handedness) == 1:
            ###MAGIC FINGER###
            if CursorControl == True:
              xlinearray.insert(0,int(image_width-xCoord/ScreenWidth*image_width))
              ylinearray.insert(0,int(yCoord/ScreenHeight*image_height))
              Rarray.insert(0, random.randint(0,50))
              Garray.insert(0, random.randint(0,50))
              Barray.insert(0, random.randint(0,50))
              if len(xlinearray) > int(DistanceFromScreen/1.5):
                xlinearray = xlinearray[0:int(DistanceFromScreen/1.5)]
                ylinearray = ylinearray[0:int(DistanceFromScreen/1.5)]
              #DRAW LINE BY LOOPING THROUGH ARRAY, NEWEST TO OLDEST, SO THAT IT MAKES A TIMELINE FROM CURRENT TO PAST
              for i in range(1,len(xlinearray)):               
                #ARRAY HANDLER
                if xlinearray[i] < 1:
                  xlinearray[i] = 1
                if ylinearray[i] < 1:
                  ylinearray[i] = 1
                #GENERATE A TRACING LINE
                cv2.line(image,(xlinearray[i-1],ylinearray[i-1]),(xlinearray[i],ylinearray[i]),(Rarray[i],Garray[i],Barray[i]),3)
 
            #DRAW MAIN ELLIPSE  
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*0.8),int(HandHeight*0.8)),RotationAngle,270+ActiveHandCount*3,270+ActiveHandCount*3+45,(255, 255, 255),int(60/DistanceFromScreen/2)+1)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*0.8),int(HandHeight*0.8)),RotationAngle,180+ActiveHandCount*3,180+ActiveHandCount*3+45,(255, 255, 255),int(60/DistanceFromScreen/2)+1)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*0.8),int(HandHeight*0.8)),RotationAngle,90+ActiveHandCount*3,90+ActiveHandCount*3+45,(255, 255, 255),int(60/DistanceFromScreen/2)+1)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*0.8),int(HandHeight*0.8)),RotationAngle,ActiveHandCount*3,ActiveHandCount*3+45,(255, 255, 255),int(60/DistanceFromScreen/2)+1)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth),int(HandHeight)),RotationAngle,0,360,(0, 127, 255),int(60/DistanceFromScreen/2))
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*1.1),int(HandHeight*1.1)),RotationAngle,90+abs(int(ActiveHandCount*4)),90+abs(int(ActiveHandCount*4))+120,(242, 255, 255),int(60/DistanceFromScreen/2))
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*1.2),int(HandHeight*1.2)),RotationAngle,-abs(int(ActiveHandCount*6)),-abs(int(ActiveHandCount*6))+120,(0, 127, 255),int(60/DistanceFromScreen/2))
 
            if CursorControl == True:
              if xCoordpinky == 0:
                xCoordpinky = 1
              if yCoordpinky == 0:
                yCoordpinky = 1
              if xCoordpinkyknuckle == 0:
                xCoordpinkyknuckle = 1
              if yCoordpinkyknuckle == 0:
                yCoordpinkyknuckle = 1
              if xCoordring == 0:
                xCoordring = 1
                
              # IF HAND IS CLOSE TO CAMERA, MINIMIZE ALL
              HandArea = math.pi*HandWidth*HandHeight
              ImageArea = image_height*image_width
              if ImageArea*0.90 < HandArea:
                keyboard.send('windows+h')
                time.sleep(1.5)
              # HandArea = math.pi*HandWidth*HandHeight
              # ImageArea = image_height*image_width
              # if ImageArea*0.90 < HandArea:
              #   keyboard.send('windows+m')
              #   time.sleep(1)
 
              #OPEN TASK VIEW
              if abs((xCoordpinky-xCoordthumb)) < 150/DistanceFromScreen and abs((yCoordpinky-yCoordthumb)) < 150/DistanceFromScreen and abs((xCoordpinkyknuckle-xCoordindexknuckle)) > 150/DistanceFromScreen:
                keyboard.send('windows+tab')
                time.sleep(0.8)
              
              #RIGHT CLICK
              if (yCoordring > yCoordringknuckle and yCoordpinky < yCoordwrist and yCoordindex < yCoordwrist and yCoordmiddle < yCoordmiddleknuckle and (yCoordindex <= yCoordindexmidknuckle) and PINKYDOWN == False):
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,xCoordmiddle,yCoordmiddle,0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,xCoordmiddle,yCoordmiddle,0,0)
                time.sleep(0.25)
                
              #SCROLL UP (RIGHT HAND)
              if (xCoordthumb > xCoordindexknuckle and yCoordpinky < yCoordwrist and yCoordindex < yCoordwrist and LeftHand == False and yCoordmiddle < yCoordmiddleknuckle and xCoordthumb < xCoordpinky and PINKYDOWN == False):
                UpCount += 1
                DownCount = 0
                if UpCount >= 30:
                  mouse.wheel(4)
                elif UpCount >= 20:
                  mouse.wheel(2)
                else:
                  mouse.wheel(1)              
 
              #SCROLL UP (LEFT HAND)
              if (xCoordthumb < xCoordindexknuckle and yCoordpinky < yCoordwrist and LeftHand == True and yCoordindex < yCoordwrist and yCoordmiddle < yCoordmiddleknuckle and xCoordthumb > xCoordpinky and PINKYDOWN == False):
                UpCount += 1
                DownCount = 0
                if UpCount >= 30:
                  mouse.wheel(4)
                elif UpCount >= 20:
                  mouse.wheel(2)
                else:
                  mouse.wheel(1)
 
              #LEFT CLICK (DOWN)
              elif (yCoordindex > yCoordindexuppernuckle) and LeftClickDown == False and CursorControl == True and yCoordindex < yCoordwrist and yCoordpinky < yCoordwrist and yCoordmiddle < yCoordmiddleknuckle and PINKYDOWN == False:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,xCoordmiddle,yCoordmiddle,0,0)
                LeftClickDown = True
              #LEFT CLICK (UP)
              elif (yCoordindex <= yCoordindexuppernuckle) and LeftClickDown == True and CursorControl == True and yCoordindex < yCoordwrist and yCoordpinky < yCoordwrist and yCoordmiddle < yCoordmiddleknuckle:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,xCoordmiddle,yCoordmiddle,0,0)
                LeftClickDown = False
              
              #SCROLL DOWN
              elif (yCoordpinky > yCoordpinkyknuckle) and CursorControl == True and yCoordindex < yCoordwrist and yCoordpinky < yCoordwrist and yCoordmiddle < yCoordmiddleknuckle and yCoordthumbknuckle > yCoordpinkyknuckle:
                DownCount += 1
                UpCount = 0
                if DownCount >= 30:
                  mouse.wheel(-4)
                elif DownCount >= 20:
                  mouse.wheel(-2)
                else:
                  mouse.wheel(-1)
                  
            #DRAW THE OUTLINE ON THE HAND
            mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(thickness=2, circle_radius=1, color=(0,127,255))
            )
        
          #SET RING THICKNESS BASED ON HOW LONG FULL HAND HAS BEEN SHOWN
          if HandCounter*6 <= 120:
            RingThickness = 3
          elif HandCounter*6 <= 240:
            RingThickness = 5
          else:
            RingThickness = 7
            
          #IF HAND IS STILL APPEARING, GENERATE IRON MAN STUFF WHILE LOADING
          if yRealimagemiddleknuckle*image_height > yRealimagemiddle*image_height and HandCounter*6 <= 360:
            if HandCounter*6 <= 120:
              cv2.ellipse(image,(int(xAnimation),int(yAnimation)),(int(HandWidth*1.65),int(HandHeight*0.1)),45,0,int(HandCounter*HandCounter/2)+90,(int(HandCounter*4.25), int(HandCounter*4.25), int(HandCounter*4.25)),4)
            elif HandCounter*6 <= 240:
              cv2.ellipse(image,(int(xAnimation),int(yAnimation)),(int(HandWidth*1.65),int(HandHeight*0.1)),45,0,360,(int(HandCounter*4.25), int(HandCounter*4.25), int(HandCounter*4.25)),4)
              cv2.ellipse(image,(int(xAnimation),int(yAnimation)),(int(HandWidth*1.65),int(HandHeight*0.1)),315,90,int(HandCounter*HandCounter/3)+90,(int(HandCounter*4.25), int(HandCounter*4.25), int(HandCounter*4.25)),4)
            elif HandCounter*6 <= 360:
              cv2.ellipse(image,(int(xAnimation),int(yAnimation)),(int(HandWidth*1.65),int(HandHeight*0.1)),45,0,360,(int(HandCounter*4.25), int(HandCounter*4.25), int(HandCounter*4.25)),4)
              cv2.ellipse(image,(int(xAnimation),int(yAnimation)),(int(HandWidth*1.65),int(HandHeight*0.1)),315,0,360,(int(HandCounter*4.25), int(HandCounter*4.25), int(HandCounter*4.25)),4)
              cv2.ellipse(image,(int(xAnimation),int(yAnimation)),(int(HandWidth*1.65),int(HandHeight*0.1)),90,0,int(HandCounter*5)+60,(int(HandCounter*4.25), int(HandCounter*4.25), int(HandCounter*4.25)),4)
              
            cv2.ellipse(image,(xAnimation,yAnimation),(HandWidth,HandHeight),RotationAngle,0,int(HandCounter*6),(0, int(HandCounter*2.116), int(HandCounter*4.25)),5)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*1.1),int(HandHeight*1.1)),RotationAngle,90+abs(int(359-HandCounter*6)),90+360,(0, abs(int(HandCounter*2.116)), int(HandCounter*4.25)),4)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*1.2),int(HandHeight*1.2)),RotationAngle,180,180+abs(int(HandCounter*6)),(0, abs(int(HandCounter*2.116)), abs(int(HandCounter*4.25))),3)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*(HandCounter*0.0132)),int(HandHeight*(HandCounter*0.0132))),RotationAngle,int(HandCounter*HandCounter/2),int(HandCounter*HandCounter/2+60),(255, 255, 255),RingThickness)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*(HandCounter*0.0132)),int(HandHeight*(HandCounter*0.0132))),RotationAngle,180+int(HandCounter*HandCounter/2),180+int(HandCounter*HandCounter/2+60),(255, 255, 255),RingThickness)
            cv2.ellipse(image,(xAnimation,yAnimation),(int(HandWidth*1.675),int(HandHeight*1.675)),RotationAngle,0,-int(HandCounter*6),(int(HandCounter*4.25), int(HandCounter*4.25), int(HandCounter*4.25)),RingThickness-2)
 
            HandCounter += 2; LostHandCount = 0
          
      #FRAME WITH NO HAND
      else:
        LostHandCount += 1; xlinearray = []; ylinearray = []; xCoordarray = []; yCoordarray = []
        if LostHandCount >= 20:
          HandCounter = 0
          ActiveHandCount = 0
          HandShown = False
        
      #FLIP, RESIZE, AND SHOW IMAGE. 
      window_name = "MK Motion Control"
      
      image = cv2.flip(image,1)
      if CursorControl == True:
        text = "Hold 'x' to deactivate"
        cv2.putText(image, text, (int(0), int(ScreenHeight/30)), cv2.FONT_HERSHEY_SIMPLEX, int(ScreenHeight/500), (0, 127, 255), 2)
        image = cv2.flip(image,1)
      else:
        text = "Hold 'c' to activate cursor"
        cv2.putText(image, text, (int(0), int(ScreenHeight/30)), cv2.FONT_HERSHEY_SIMPLEX, int(ScreenHeight/500), (0, 127, 255), 2)
        image = cv2.flip(image,1)
      
      # if HandCounter*6 > 360:
      #   image = cv2.flip(image,1)
      #   text = "Mouse Sensitiv. = " + str(DistanceFromScreen)
      #   cv2.putText(image, text, (int(0), int(ScreenHeight/1.6)), cv2.FONT_HERSHEY_SIMPLEX, int(ScreenHeight/500), (0, 127, 255), 2)
      #   image = cv2.flip(image,1)
 
      if HandShown == False:
        if cv2.waitKeyEx(5) == 2490368 and ImageSizeMod > 1:
          ImageSizeMod -= 1
        elif cv2.waitKeyEx(5) == 2621440 and ImageSizeMod < 7:
          ImageSizeMod += 1
 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )
        cv2.imshow('MK Motion Control', cv2.flip(cv2.resize(image,(int(round(ScreenWidth/ImageSizeMod)),int(round(ScreenHeight/ImageSizeMod)))), 1))
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
      else:
        cv2.imshow('MK Motion Control', cv2.flip(cv2.resize(image,(int(round(ScreenWidth/ImageSizeMod)),int(round(ScreenHeight/ImageSizeMod)))), 1))
      
      #SET WINDOW AS TOP.
      cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
 
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
  cap.release()
 
if __name__ == '__main__':
  main()
