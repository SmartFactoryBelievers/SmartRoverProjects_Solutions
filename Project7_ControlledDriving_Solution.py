# Project 7

# Learning to program, writing functions, using motor control outputs, adding complex logic

# Build the the Project 7 circuit and drive the rover with button presses A, B, and C

# Set the controls for the rover for 3 unique commands, and possibly more?

#Challenge 1
# Try changing the drive functions to switch the driving directions for forward/backwards and turning

#Challenge 2
# Add new drive functions to change the driving patterns for each button press

#Challege 3
# Incorporate the button press timer from project 5 to add Simon Says to driving functions

#Challege 4
# See how B uses a double If to see if its pressed and then released or held? Can you try
# something similar for A and C to create different commands there too?

#Challenge 5
# Replace the length-3 snap connector with the phototransistor - now all three buttons
# are light dependant. Try controlling the rover to stay in the light.

#Importing libraries
# Here we want the time and sleep for timing and GPIO for the Pi's pins
import time
from time import sleep
import RPi.GPIO as GPIO

#Let's define variables so we can use them later
Left_Forward_Pin = 36 #the internal Pi pin number that goes to snap 1
Left_Backward_Pin = 11 #the internal Pi pin number that goes to snap 2
Right_Forward_Pin = 12 #the internal Pi pin number that goes to snap 3
Right_Backward_Pin = 35 #the internal Pi pin number that goes to snap 4
A_Pin = 40 #the internal Pi pin number that goes to snap 7
C_Pin = 38 #the internal Pi pin number that goes to snap 6

#Here we can define the timing variables for the driving functions, in seconds
Forward_Time = 2
Backward_Time = 1
Left_Turn_Time = 0.5
Right_Turn_Time = 0.5
Wait_Time = 0.5

#Setting up our pins
GPIO.setmode(GPIO.BOARD)
#Our output pins, start off
GPIO.setup(Left_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Left_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Forward_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Right_Backward_Pin, GPIO.OUT, initial=GPIO.LOW)
#Our input pin from the button
GPIO.setup(A_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
  
# Here we are creating a timer function to record the duration of the button press
def button_press_timer():
  Start_Time = time.time() #start the timer
  while GPIO.input(Button_Pin): #while the button is pressed...
    print("Button Pressed")
  return round(time.time() - Start_Time,2) #stop the timer, return elapsed time
# For challenge 3, try uncommenting the Press_Time statements, then use it for the
# the drive commands time arguments

while True: #Looping over and over again
  sleep(0.5)
  
  # Only pressing A
  if GPIO.input(A_Pin) and not GPIO.input(C_Pin): #only pressing A
    # For challenge 4, you can use a sleep delay and second if, else to see
    # whether A was pressed and released or held
    sleep(0.5)
    #Press B and hold, check if still pressed after delay
    if GPIO.input(A_Pin) and not GPIO.input(A_Pin):
      drive_forward(Forward_Time)
      drive_backward(Backward_Time)
    else:
      Press_Time = button_press_timer(A_Pin) # For challenge 3
      drive_forward(Forward_Time)
    
  # Only pressing C
  if GPIO.input(C_Pin) and not GPIO.input(A_Pin): #only pressing C
    # For challenge 4, you can use a sleep delay and second if, else to see
    # whether C was pressed and released or held
    Press_Time = button_press_timer(C_Pin) # For challenge 3
    drive_backward(Backward_Time)
    
  # Pressing B, we can use timing to determine if it's released or held
  if GPIO.input(C_Pin) and GPIO.input(A_Pin):
    sleep(0.5)
    #Press B and hold, check if still pressed after delay
    if GPIO.input(C_Pin) and GPIO.input(A_Pin):
      drive_left_turn(Left_Turn_Time)
    # Press B and released, not still pressed after delay
    else:
      drive_right_turn(Right_Turn_Time)
