# Project 6

# Learning to program, writing functions, using motor control outputs, adding loop complexity

# Build the the Project 6 circuit and have the rover be controlled by ambient light
# Turn down the ligth and point a flashlight at the rover to direct it

#Challenge 1
# Try changing the drive functions to switch the driving directions

#Challenge 2
# Add new drive functions to change its light seeking spin pattern

#Challege 3
# Add the 100 Ohm resistor in series with the photoresistor to increase light sensitivity

#Challege 4
# With the modulo operator, have the rover alternate left or right spins in light searching

#Challenge 5
# After a certain amount of time, have the rover spin to look for light

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
Photo_Pin = 38 #the internal Pi pin number that goes to snap 6

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
#Our input pin from the button
GPIO.setup(Photo_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
  
# For challenge 4, we will use a dummy variable to help with modulo operator
count = 0
# Replace the True with the modulo operator statement as %, which means remainder in division
# So modulo 2 keeps track of odd and even presses since even divided by 2 has remainder of 0
# To use this as a logical, let's try count % 2 == 0

# For challenge 5, we will set a maximum light search time for the loop
Max_Search_Time = 4 #seconds
# If the rover has not found light by then, we can get out of the loop with a break statement
# break exits the innermost loop and allows the rover to return to the first sleep command

while True: # Continuous outer while loop
  sleep(0.25)
  count = count + 1 # Increment the counter for the modulo
  
  # If the phototransistor detects enough light, drive towards it
  if GPIO.input(Photo_Pin):
    # For challenges 1 and 2, change driving instructions here
    drive_forward(Forward_Time)
    
  # If there's not enough light, let's look for it by spinning the rover
  else:
  # For challenge 5, we can use the timer function to control the light search
    Start_Time = time.time()
    while not(GPIO.input(Photo_Pin)):
      Elapsed_Time = round(time.time() - Start_Time,2)
      print('Not enough light, searching for more')
      
    if Elapsed_Time < Max_Search_Time: # Try changing the True to a comparative (<) between
      # Elapsed_Time and Max_Search_Time for challenge 5
      
      if count % 2 == 0: # Try changing the True to the modulo for challenge 4
        drive_left_turn(Left_Turn_Time)
        sleep(Wait_Time)
        
      else: # For challenge 4, modulo uses these drive commands on odd loops
        drive_right_turn(Right_Turn_Time)
        sleep(Wait_Time)
    else:
      break # Exits the loop after Max Search Time exceeded
