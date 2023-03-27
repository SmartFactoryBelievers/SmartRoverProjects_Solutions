# Project 5

# Learning to program, writing functions, using motor control outputs, adding callback function

# Build the the Project 5 circuit and drive the rover through button pushes, Simon Says style
# Press and hold the button to drive for that duration

#Challenge 1
# Try changing the drive functions to switch the driving directions

#Challenge 2
# Add new drive functions to activate in the loop to create a new path

#Challege 3
# Use the modulo opertor to change the driving directions based on even or odd numbered presses

#Challege 4
# With the modulo, add new dirivng functions for even or odd numbered presses

#Importing libraries
# Here we want the sleep function for timing and GPIO for the Pi's pins
from time import sleep
import RPi.GPIO as GPIO
# We also now are using the general time library for the timer function
import time

#Let's define variables so we can use them later
Left_Forward_Pin = 36 #the internal Pi pin number that goes to snap 1
Left_Backward_Pin = 11 #the internal Pi pin number that goes to snap 2
Right_Forward_Pin = 12 #the internal Pi pin number that goes to snap 3
Right_Backward_Pin = 35 #the internal Pi pin number that goes to snap 4
Button_Pin = 38 #the internal Pi pin number that goes to snap 6

#Setting up our pins
GPIO.setmode(GPIO.BOARD)
#Our output pins, start off
GPIO.setup(Left_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Left_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)
#Our input pin from the button
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Let's write some driving functions we can use later to program a pathdef drive_forward():
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
  
# Here we are creating a timer function to record the duration of the button press
def button_press_timer():
  Start_Time = time.time() #start the timer
  while GPIO.input(Button_Pin): #while the button is pressed...
    print("Button Pressed")
  return round(time.time() - Start_Time,2) #stop the timer, return elapsed time

# For challenges 3 and 4, we will use a dummy variable to help with modulo operator
count = 0
# Replace the True with the modulo operator statement as %, which means remainder in division
# So modulo 2 keeps track of odd and even presses since even divided by 2 has remainder of 0
# To use this as a logical, let's try count % 2 == 0

while True: #Looping over and over again
  sleep(0.25)
  
  # If the button is pressed, let's use the timer function to see how long
  if GPIO.input(Button_Pin):
    Button_Time = button_press_timer()
    print('Button pressed ' + str(Button_Time) + ' seconds')
    
    if count % 2 == 0: # Try changing the True to the modulo for challenges 3 and 4
      
      #For challenges 1 and 2, try adding new driving functions here
      drive_forward(Button_Time)
    
    else: # To be used in challenges 3 and 4
      drive_backward(Button_Time)
      # Add other drive functions here for odd button presses
      
    count = count + 1 # We increment the counter for the next button press
