# Project 3

# Learning to program, writing functions, and using inputs and outputs

# Build the the Project 3 circuit and control a LED and buzzer with a selector
# Press and hold buttons A, B, and C on the selector

#Challenge 1
# Try changing the Pin_On and Pin_Off variables to change the blinking pattern

#Challenge 2
# Replace the color LED with buzzer or white LED to try other outputs

#Challenge 3
# Try changing input pins A and C in the While loop to switch what A and C do when pressed

#Challenge 4
# Try changing output pins LED and Buzzer in the While loop to switch what A and C do when pressed

#Challenge 5
# Try switching the order of the LED and Buzzer functions for a cool lightshow when pressing B

#Importing libraries
# Here we want the sleep function for timing and GPIO for the Pi's pins
from time import sleep
import RPi.GPIO as GPIO

#Let's define variables so we can use them later
A_Pin = 40 #the internal Pi pin number that goes to snap 7
C_Pin = 38 #the internal Pi pin number that goes to snap 6
LED_Pin = 12 #the internal Pi pin number that goes to snap 3
Buzzer_Pin = 35 #the internal Pi pin number that goes to snap 4

# For challenge 1, we can try different values here to blink in new patterns
Pin_On = 3 #duration of LED flash, seconds
Pin_Off = 0.5 #duration in between flashes, seconds

#Setting up our pins
GPIO.setmode(GPIO.BOARD)

#Our output pins, start off
GPIO.setup(LED_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Buzzer_Pin, GPIO.OUT, initial=GPIO.LOW)

#Our input pins from the selector
GPIO.setup(A_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Let's write some functions we can use to make the coding easier
# For a code snippet we will reuse, we can turn it into a function to call later
# The function name is in blue, and then the arguments it takes are in parentheses

#Here's a function for seeing if a selector button is pressed
# So, read_selector_button reads and returns the value of In_Pin
# This will be helpful for reading the A and C button pins
def read_selector_button(In_Pin):
  return GPIO.input(In_Pin)

#Here's a function for turning an output pin on
#So, output_pin_on takes in the pin number and turns it on after a defined delay
def output_pin_on(Out_Pin, Delay):
  sleep(Delay)
  GPIO.output(Out_Pin, GPIO.HIGH)
  
#Here's a function for turning an output pin off, can you fill in the missing pieces?
# Replace the ?? with the variables and then uncomment
def output_pin_off(Out_Pin, Delay):
  sleep(Delay) #wait the Delay
  GPIO.output(Out_Pin, GPIO.LOW) #turn the Out_Pin off
  
while True: #Looping over and over again
  
  # Here we can use the functions we defined to read buttons and control outputs
  # For the challenges, try changing the button and output pins in the below code

  # If A is pressed and C is not, let's blink the LED
  if read_selector_button(A_Pin) and not(read_selector_button(C_Pin)):
    output_pin_on(LED_Pin, Pin_Off)
    output_pin_off(LED_Pin, Pin_On)
    
  # If C is pressed and A is not, let's buzz the buzzer
  if read_selector_button(C_Pin) and not(read_selector_button(A_Pin)):
    output_pin_on(Buzzer_Pin, Pin_Off)
    output_pin_off(Buzzer_Pin, Pin_On)
    
  # If A and C are both pressed, by pressing B, maybe we can flash both LED and buzzer?
  # Replace the ?? with the LED_Pin and Buzzer_Pin variables and then uncomment
  if read_selector_button(A_Pin) and read_selector_button(C_Pin):
    output_pin_on(LED_Pin, Pin_Off)
    output_pin_off(Buzzer_Pin, Pin_On)
    output_pin_on(LED_Pin, Pin_Off)
    output_pin_off(Buzzer_Pin, Pin_On)
    
  # Wait 1 second to reset
  sleep(1)
