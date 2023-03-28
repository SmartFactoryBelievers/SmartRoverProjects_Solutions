# Project 12

# Using the Pi camera to capture and analyze the surroudning light levels

# Build the the Project 12 circuit and drive the rover to seek out light

#Challenge 1
# Try changing the Left and Right Thresholds to force different turning patterns

#Challenge 2
# Try using the modulo function and loop counter to go from forward to reverse every few cycles

#Challege 3
# Can you add a timer to the loop to do a spin after a 30 seconds of searching?

#Challege 4
# Can you set the drive time duration based on the ratio of left-to-right light?

#Importing libraries
# Here we want sleep for timing, GPIO for the Pi's pins, & picamera for the Pi's camera
from time import sleep
import time
import RPi.GPIO as GPIO
from picamera import PiCamera
# We will also need PiRGBArray and cv2 for computer vision/image processing
from picamera.array import PiRGBArray
import cv2
# Numpy is a great numerical tools package to help with the math required
import numpy as np

#Let's define variables so we can use them later
Left_Forward_Pin = 36 #the internal Pi pin number that goes to snap 1
Left_Backward_Pin = 11 #the internal Pi pin number that goes to snap 2
Right_Forward_Pin = 12 #the internal Pi pin number that goes to snap 3
Right_Backward_Pin = 35 #the internal Pi pin number that goes to snap 4

#Here we can define the timing variables for the driving functions, in seconds
Forward_Time = 2
Backward_Time = 1
Left_Turn_Time = 0.5
Right_Turn_Time = 0.5
Wait_Time = 1

#Setting up our pins
GPIO.setmode(GPIO.BOARD)
#Our output pins, start off
GPIO.setup(Left_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Left_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)

#Let's write some driving functions we can use later
def drive_forward(time):
  GPIO.output(Left_Forward_Pin, GPIO.HIGH) #Left motor forward
  GPIO.output(Right_Forward_Pin, GPIO.HIGH) #Right motor forward
  sleep(time)
  GPIO.output(Left_Forward_Pin, GPIO.LOW) #Left motor off
  GPIO.output(Right_Forward_Pin, GPIO.LOW) #Right motor off
  print('forward')
  sleep(1)
  
def drive_left_turn(time):
  GPIO.output(Left_Backward_Pin, GPIO.HIGH) #Left motor backward
  GPIO.output(Right_Forward_Pin, GPIO.HIGH) #Right motor forward
  sleep(time)
  GPIO.output(Left_Backward_Pin, GPIO.LOW) #Left motor off
  GPIO.output(Right_Forward_Pin, GPIO.LOW) #Right motor off
  print('left turn')
  sleep(1)
  
def drive_right_turn(time):
  GPIO.output(Left_Forward_Pin, GPIO.HIGH) #Left motor forward
  GPIO.output(Right_Backward_Pin, GPIO.HIGH) #Right motor backward
  sleep(time)
  GPIO.output(Left_Forward_Pin, GPIO.LOW) #Left motor off
  GPIO.output(Right_Backward_Pin, GPIO.LOW) #Right motor off
  print('right turn')
  sleep(1)
  
def drive_backward(time):
  GPIO.output(Left_Backward_Pin, GPIO.HIGH) #Left motor backward
  GPIO.output(Right_Backward_Pin, GPIO.HIGH) #Right motor backward
  sleep(time)
  GPIO.output(Left_Backward_Pin, GPIO.LOW) #Left motor off
  GPIO.output(Right_Backward_Pin, GPIO.LOW) #Right motor off
  print('backward')
  sleep(1)
  
#Setting up the camera
camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

#Setting Min and Max values for Hue, Saturation (Grayness), and Value (Lightness)
Light_Min = np.array([0,50,155], np.uint8)
Light_Max = np.array([255,255,255], np.uint8)

# Ambient light percentage of one side to the other, threshold for turning the rover
# For challenge 1, try adjusting these values to force more or fewer turns
Left_Threshold = 51
Right_Threshold = 51

# For challenge 2, we will use a dummy variable to help with modulo operator
count = 0
# Replace the True with the modulo operator statement as %, which means remainder in division
# So modulo 2 keeps track of odd and even presses since even divided by 2 has remainder of 0
# To use this as a logical, let's try count % 2 == 0

# For challenge 2, we can use the timer function to control the light seach
Start_Time = time.time()
Max_Search_Time = 30 #seconds

# For challenge 4, we can initialize a variable for Light Intensity to scale the turn durations
Light_Intensity = 1

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  #Capturing image from camera and converting to HSV format
  sleep(3)
  Image = frame.array
  hsv = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
  
  # Analyzing the value (lightness) layer of the image (3rd layer)
  Light = hsv[:,:,2]
  
  # Calculating the total light in the left and right halves of the image
  Left_Light = sum(sum(Light[:,0:320]))
  Right_Light = sum(sum(Light[:,320:]))
  
  # Determining the percentage of light of the left and right halves of the image
  Left_Light_Perc = Left_Light / sum(sum(Light))
  Right_Light_Perc = Right_Light / sum(sum(Light))
  print('L = ' + str(Left_Light_Perc) + ' and R = ' + str(Right_Light_Perc))
  
  # For challenge 3, determining time passed since forward drive
  Elapsed_Time = round(time.time() - Start_Time,2)
  
  # For challenge 4, let's find the ratio of the max light to the min light
  # We can set this as the intensity with np.max([Left_Light_Perc, Right_Light_Perc])
  # and np.min([Left_Light_Perc, Right_Light_Perc]), respectively
  Light_Intensity = np.max([Left_Light_Perc, Right_Light_Perc]) / np.min([Left_Light_Perc, Right_Light_Perc])
  
  # If the left side is lighter than the threshold, turn left
  if Left_Light_Perc > Left_Threshold/100:
    drive_left_turn(Left_Turn_Time * Light_Intensity)
    
  # If the right side is lighter than the threshold, turn right
  else:
    if Right_Light_Perc > Right_Threshold/100:
      drive_right_turn(Right_Turn_Time * Light_Intensity)
      
    # If neither side exceeds the threshold, drive forward (or reverse?)
    else:
      if Elapsed_Time < Max_Search_Time: # Try changing the True to a comparitive (<) between
        # Elapsed_Time and Max_Search_Time for challenge 3

        if count % 2 == 0: # Try changing the True to the modulo for challenge 2
          drive_forward(Forward_Time)
        else: # For challenge 2, modulo uses these drive commands on odd loops
          drive_backward(Backward_Time)

        count = count + 1 # Increment the counter for the modulo
      else: # If max search time exceeded, spin and look elsewhere for challenge 3
        drive_left_turn(Left_Turn_Time * 2)
        # Reset the timer for a new searching period
        Start_Time = time.time()
        print('here')
    
  sleep(Wait_Time)
  #Clearing image cache
  rawCapture.truncate(0)
