# Project 10

# Using the Pi cameraera to capture and analyze the color profile of objects

# Build the Project 10 circuit and indicate the color of objects with LED and buzzer

#Challenge 1
# Try swapping the LED and buzzer outputs in the code and then also on the rover

#Challenge 2
# Try writing a function to handle the LED and buzzer so it can be called after each color

#Challege 3
# Try adding a margin that the argmax for Color must exceed to be considered a certain color

#Challege 4
# Try adding a memory variable for the last color identified and activate flashes and buzzes
# a new LED or buzzer output based on the pattern, like Red then Green

#Importing libraries
# Here we want sleep for timing, GPIO for the Pi's pins, & picamera for the Pi's camera
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
# Numpy is a great numerical tools package to help with the math required
import numpy as np

#Let's define variables so we can use them later
LED_Pin = 35 #the internal Pi pin number that goes to snap 4
Buzzer_Pin = 12 #the internal Pi pin number that goes to snap 3
Button_Pin = 38 #the internal Pi pin number that goes to snap 6

#Setting up our pins
GPIO.setmode(GPIO.BOARD)
#Our output pins, start off
GPIO.setup(LED_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Buzzer_Pin, GPIO.OUT, initial=GPIO.LOW)
#Our input pins, start down
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setting up camera for analysis and to emphasize colors
camera = PiCamera()
camera.resolution = (640, 480)camera.framerate = 30
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

# For challenge 2, let's create a function like we've done before for outputs
# It should have output_pin and delay time arguments to turn them High and then Low
def your_function(output_pin, delay):
  sleep(delay)
  GPIO.output(output_pin, GPIO.HIGH)
  sleep(delay)
  GPIO.output(output_pin, GPIO.LOW)
  
# For challenge 3, let's set a threshold the max color must exceed
# This will help the camera avoid mistakes in bad lighting or glare
Col_Margin = 0.8
# Let's check if the max * margin > mid
# with max as np.max(RGB_Array) and mid as np.median(RGB_Array)

#Looping with different images to determine object colors upon button press
print('Ready to take photo')
while True:
  # Press the push button to capture an image
  if GPIO.input(Button_Pin) == True:
    sleep(2)
    print('Photo taken')
    camera.capture(Image,'rgb')
    RGB_Array = []
    
    # For each of red, green, and blue, calculate the most prominent color through means
    for col in range(0,3):
    RGB_Array.append(np.mean(Image[:,:,col]-np.mean(Image)-np.mean(Noise[:,:,col])))
    # For challenge 3, replace the True with the logical statement for the margin
    
    if np.max(RGB_Array) * Col_Margin > np.median(RGB_Array):
      Color = RGB_Text[np.argmax(RGB_Array)]
      print(Color)
    else:
      print('No prominent color found')
      
    # For challenge 4, let's look for a pattern like Red then Color
    # We can use an if statement to see if the Last_Color was Red
    # Replace this True with a logical to check, remember it's ==, not = here
    if Last_Color == 'Red':
      
      # Activate outputs based on the determined object color
      if Color == 'Red': #LED for Red object
        GPIO.output(LED_Pin, GPIO.HIGH) #LED on
        sleep(2)
        GPIO.output(LED_Pin, GPIO.LOW) #LED off

      if Color == 'Green': #Buzzer for Green object
        GPIO.output(Buzzer_Pin, GPIO.HIGH) #Buzzer on
        sleep(2)
        GPIO.output(Buzzer_Pin, GPIO.LOW) #Buzzer off

      if Color == 'Blue': #LED and Buzzer for Blue object
        GPIO.output(LED_Pin, GPIO.HIGH) #LED on
        GPIO.output(Buzzer_Pin, GPIO.HIGH) #Buzzer on
        sleep(2)
        GPIO.output(LED_Pin, GPIO.LOW) #LED off
        GPIO.output(Buzzer_Pin, GPIO.LOW) #Buzzer off

    # For challenge 4, update Last_Color after outputs
    Last_Color = Color
    print('Ready to take photo')
