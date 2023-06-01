# Project 4

# Learning to program, writing functions, and using motor control outputs

# Build the the Project 4 circuit and drive the rover along your designed path

#Challenge 1
# Try changing the drive time variable to create a new driving path

#Challenge 2
# Reorder the drive functions to create a new driving path

#Challege 3
# Create your own custom driving path using the different drive functions and time arguments

#Importing libraries
# Here we want the sleep function for timing and GPIO for the Pi's pins
from time import sleep
import RPi.GPIO as GPIO

#Let's define variables so we can use them later
Left_Forward_Pin = 36 #the internal Pi pin number that goes to snap 1
Left_Backward_Pin = 11 #the internal Pi pin number that goes to snap 2
Right_Forward_Pin = 12 #the internal Pi pin number that goes to snap 3
Right_Backward_Pin = 35 #the internal Pi pin number that goes to snap 4

#Here we can define the timing variables for the driving functions, in seconds
# For challenge 1, we can try different values here to drive in new patterns
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

#Let's write some driving functions we can use later to program a driving path
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
  
# Can you finish the function by filling in the blanks for the pins and states?
# This is a backward driving function, so both backward pins should be High then Low
# Uncomment the code when complete
def drive_backward(time):
  GPIO.output(Left_Backward_Pin, GPIO.HIGH) #Left motor backward
  GPIO.output(Right_Backward_Pin, GPIO.HIGH) #Right motor backward
  sleep(time)
  GPIO.output(Left_Backward_Pin, GPIO.LOW) #Left motor off
  GPIO.output(Right_Backward_Pin, GPIO.LOW) #Right motor off
  print('backward')
  sleep(1)
  
#Here we can use a for loop to control the number of times the code is executed
# Changing the value of range() increases the number of loops performed
for n in range(1):
  
  # Let's use the driving functions defined above to create a driving path
  # For challenges 2 and 3, try changing the driving functions and order here
  sleep(Wait_Time)
  drive_forward(Forward_Time)
  drive_left_turn(Left_Turn_Time)
  drive_backward(Backward_Time)
  drive_right_turn(Right_Turn_Time)
