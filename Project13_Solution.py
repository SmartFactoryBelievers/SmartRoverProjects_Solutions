# Project 13

# Using the Pi camera to capture and analyze the color profile of objects

# Build the the Project 13 circuit and drive the rover according to colored signs

#Challenge 1
# Try changing the colors associated with the driving commands, like flipping red and green

#Challenge 2
# Try adding a modulo operator to alternate between left and right turns on blue signs

#Challege 3
# Try setting the drive_time variable based on the promince of the color from the argmax

#Challenge 4
# Try adding a memory array for the last two colors identified and dictate driving
# based on the pattern

#Importing libraries
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import cv2

#Let's define variables so we can use them later
Left_Forward_Pin = 36 #the internal Pi pin number that goes to snap 1
Left_Backward_Pin = 11 #the internal Pi pin number that goes to snap 2
Right_Forward_Pin = 12 #the internal Pi pin number that goes to snap 3
Right_Backward_Pin = 35 #the internal Pi pin number that goes to snap 4
Button_Pin = 38 #the internal Pi pin number that goes to snap
drive_time = 1 # seconds
turns = 0 #turn counter

#Setting up our pins
GPIO.setmode(GPIO.BOARD)
#Our output pins, start off
GPIO.setup(Left_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Left_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)
#Our input pins, start down
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Let's write some driving functions we can use later to program a pathdef drive_forward():
def drive_forward(time):
  GPIO.output(Left_Forward_Pin, GPIO.HIGH) #Left motor fwd
  GPIO.output(Right_Forward_Pin, GPIO.HIGH) #R motor fwd
  sleep(time)
  GPIO.output(Left_Forward_Pin, GPIO.LOW) #Left motor fwd
  GPIO.output(Right_Forward_Pin, GPIO.LOW) #R motor fwd
  print('fwd')
  sleep(1)
  
def drive_backward(time):
  GPIO.output(Left_Backward_Pin, GPIO.HIGH) #Left motor bkwd
  GPIO.output(Right_Backward_Pin, GPIO.HIGH) #R motor bkwd
  sleep(time)
  GPIO.output(Left_Backward_Pin, GPIO.LOW) #Left motor bkwd
  GPIO.output(Right_Backward_Pin, GPIO.LOW) #R motor bkwd
  print('bkwd')
  sleep(1)
  
def drive_left_turn(time):
  GPIO.output(Left_Backward_Pin, GPIO.HIGH) #Left motor bkwd
  GPIO.output(Right_Forward_Pin, GPIO.HIGH) #R motor fwd
  sleep(time)
  GPIO.output(Left_Backward_Pin, GPIO.LOW) #Left motor bkwd
  GPIO.output(Right_Forward_Pin, GPIO.LOW) #R motor fwd
  print('left turn')
  sleep(1)
  
def drive_right_turn(time):
  GPIO.output(Left_Forward_Pin, GPIO.HIGH) #Left motor bkwd
  GPIO.output(Right_Backward_Pin, GPIO.HIGH) #R motor fwd
  sleep(time)
  GPIO.output(Left_Forward_Pin, GPIO.LOW) #Left motor bkwd
  GPIO.output(Right_Backward_Pin, GPIO.LOW) #R motor fwd
  print('right turn')
  sleep(1)
  
# Setting up camera for analysis and to emphasize colors
camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
camera.framerate = 30
sleep(2) #let the cameraera settle
camera.iso = 100
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
gain_set = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = gain_set

# Prepping for image analysis and eliminating background noise
data = np.empty((640,480,3),dtype=np.uint8)
noise = np.empty((640,480,3),dtype=np.uint8)
#Images are stored in a 3D array with each pixel having Red, Green, and Blue values
x,y = np.meshgrid(np.arange(np.shape(data)[1]),np.arange(0,np.shape(data)[0]))
rgb_text = ['Blue', 'Green','Red'] #Array for naming colors bgr
camera.capture(noise, 'bgr')
noise = noise-np.mean(noise) # Background 'noise

#Setting Min and Max values for Hue, Saturation (Grayness), and Value (Lightness)
BGR_HSV_Min = np.array([121, 61, 0], np.uint8)
BGR_HSV_Max = np.array([150, 90, 30], np.uint8)

#Looping with different images to determine object colors
print('Ready')
while True:
  #Press the push button to capture an image
  if GPIO.input(Button_Pin) == True:
    sleep(2)
    print('Photo taken')
    camera.capture(data,'bgr')
    hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
    mean_array,std_array = [],[]
    for ii in range(0,3):
      #Calculating averages of each color to determine most prominent
      mean_array.append(np.mean(data[:,:,ii]-np.mean(data)-np.mean(noise[:,:,ii])))
     color_picker = np.argmax(mean_array)
     Color = rgb_text[color_picker]
     print(Color)
    #print(np.mean(np.mean(hsv[ :, :, 0])))
    color_view = (hsv[ :, :, 0] >= BGR_HSV_Min[color_picker]) & \
    (hsv[ :, :, 0] <= BGR_HSV_Max[color_picker])
    print(sum(sum(color_view)))
    target_color = np.mean(np.mean(hsv[:, :, 0][color_view]))
    print(target_color)
    sleep(3)
    camera.close()
    
    #Setting up the video camera
    vid_camera = PiCamera()
    vid_camera.resolution = (640, 480)
    vid_camera.framerate = 30
    vid_camera.rotation = 180
    
    rawCapture = PiRGBArray(vid_camera, size=(640, 480))
    
    # Ambient Color percentage threshold for turning the rover
    Left_Threshold = 65
    Right_Threshold = 65
    Total_Threshold = 25 #percentage of target color visible
    
    #Driving duration
    drive_time = 0.1 #seconds
    
    #Color offset for hue target color
    color_offset = 7. 5
    
    for frame in vid_camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      #Capturing image from camera and converting to HSV format
      sleep(2)
      image = frame.array
      hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
      hue_view = hsv[:,:,0] #hue
      #color_view = hue_view.copy()
      target_color_view = (hue_view >= target_color - color_offset) & \
      (hue_view <= target_color + color_offset)
      print(sum(sum(target_color_view))/ (640*480))
      #color_view[~color_mask] = np.nan
      Total_Color_Perc = sum(sum(target_color_view))/ (640*480)
      Left_Color = sum(sum(target_color_view [:,0:320]))
      Right_Color = sum(sum(target_color_view [:,320:]))
      Left_Color_Perc = Left_Color / sum(sum(target_color_view ))
      Right_Color_Perc = Right_Color / sum(sum(target_color_view ))
      
      print('L = ' + str(Left_Color_Perc) + ' and R = ' + str(Right_Color_Perc))
      
      #cv2.imshow("result", image)
      
      if Total_Color_Perc > Total_Threshold/100:
        if Left_Color_Perc > Left_Threshold/100:
          drive_left_turn(drive_time)
        else:
          if Right_Color_Perc > Right_Threshold/100:
            drive_right_turn(drive_time)
          else:
            drive_forward(2.5 * drive_time)
      else:
      drive_left_turn(5 * drive_time)
      #Clearing image cache
      rawCapture.truncate(0)
