# Project 11

# Using the Pi camera to capture and analyze the color profile of objects

# Build the the Project 11 circuit and drive the rover according to colored signs

#Challenge 1
# Try changing the colors associated with the driving commands, like flipping red and green

#Challenge 2
# Try adding a modulo operator to alternate between left and right turns on blue signs

#Challege 3
# Try setting the drive time variables based on the promince of the color from the argmax

#Challenge 4
# Try adding a memory variable for the last color identified and dictate driving
# based on the pattern, like Red then Green

#Importing libraries
# Here we want sleep for timing, GPIO for the Pi's pins, & picamera for the Pi's camera
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
# Numpy is a great numerical tools package to help with the math required
import numpy as np

#Let's define variables so we can use them later
Left_Forward_Pin = 36 #the internal Pi pin number that goes to snap 1
Left_Backward_Pin = 11 #the internal Pi pin number that goes to snap 2
Right_Forward_Pin = 12 #the internal Pi pin number that goes to snap 3
Right_Backward_Pin = 35 #the internal Pi pin number that goes to snap 4
Button_Pin = 38 #the internal Pi pin number that goes to snap

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
#Our input pins, start down
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
  
# For challenge 2, we will use a dummy variable to help with modulo operator
count = 0
# Replace the True with the modulo operator statement as %, which means remainder in division
# So modulo 2 keeps track of odd and even presses since even divided by 2 has remainder of 0
# To use this as a logical, let's try count % 2 == 0

# For challenge 3, we will set the variable color intensity to scale the drive times
# First, let's define it so we can use the code as is
Color_Intensity = 1

# Setting up camera for analysis and to emphasize colors
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
sleep(2) #let the cameraera settle
camera.iso = 100
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
gain_set = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = gain_set

# Prepping for image analysis and eliminating background Noise
#Images are stored in a 3D array with each pixel having Red, Green, and Blue values
Image = np.empty((640,480,3),dtype=np.uint8)
Noise = np.empty((640,480,3),dtype=np.uint8)
RGB_Text = ['Red','Green','Blue'] #Array for naming color
# Let's remove the background 'Noise' colors to emphasis the object's color
camera.capture(Noise,'rgb')
Noise = Noise-np.mean(Noise)

#Looping with different images to determine object colors
print('Ready to take photo')
while True:

  #Press the push button to capture an image
  if GPIO.input(Button_Pin) == True:
    sleep(2)
    print('Photo taken')
    camera.capture(Image,'rgb')
    RGB_Array = []
    
    # For each of red, green, and blue, calculate the most prominent color through means
    for col in range(0,3):
      RGB_Array.append(np.mean(Image[:,:,col]-np.mean(Image)-np.mean(Noise[:,:,col])))
      Color = RGB_Text[np.argmax(RGB_Array)]
      print(Color)
      
    # For challenge 3, let's compare the most prominent color to the second most
    # We can use this ratio to set the Color_Intensity variable
    # with max as np.max(RGB_Array) and mid as np.median(RGB_Array)
    # However, the color channels can be negative, so let's use a max to keep positive
    Color_Intensity = np.max([np.max(RGB_Array) / np.median(RGB_Array), 2])
    
    # For challenge 4, let's look for a pattern like Red then Color
    # We can use an if statement to see if the Last_Color was Red
    # Replace this True with a logical to check, remember it's ==, not = here
    if Last_Color == 'Red':
      
      # Activate motor controller outputs based on the determined object color
      if Color == 'Red': #Backward for Red object
        drive_backward(Backward_Time * Color_Intensity)
        sleep(Wait_Time)
        
      if Color == 'Green': #Forward for Green object
        drive_forward(Forward_Time * Color_Intensity)
        sleep(Wait_Time)
        
      if Color == 'Blue': #Turn for Blue object
        
        if count % 2 == 0: # Try changing the True to the modulo for challenge 2
          drive_left_turn(Left_Turn_Time * Color_Intensity)
          
        else: # For challenge 2, modulo uses these drive commands on odd loops
          drive_right_turn(Right_Turn_Time * Color_Intensity)
          
        sleep(Wait_Time)
        count = count + 1 # Increment the counter for the modulo
      
    # For challenge 4, update Last_Color after outputs
    Last_Color = Color
    print('Ready to take photo')
