# Project 2

# Learning to program and using inputs and outputs

# Build the the Project 2 circuit and control a LED with a button

#Challenge 1
# Try changing the LED_On and LED_Off variables to change the blinking pattern

#Challenge 2
# Replace the color LED with buzzer or white LED to try other outputs

#Challege 3
# Replace the push button with the phototransistor and cover it with your hand - what happens?

#Challege 4
# Try changing the "If" statement from True to False - now what does the button do?

#Importing libraries
# Here we want the sleep function for timing and GPIO for the Pi's pins
from time import sleep
import RPi.GPIO as GPIO

#Let's define variables so we can use them later
Button_Pin = 38 #the internal Pi pin number that goes to snap 6
LED_Pin = 12 #the internal Pi pin number that goes to snap 3

# For challenge 1, we can try different values here to blink in new patterns
LED_On = 3 #duration of LED flash, seconds
LED_Off = 1 #duration in between flashes, seconds

#Setting up our pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_Pin, GPIO.OUT, initial=GPIO.LOW) #Output pin, start off
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Input pin, start open

while True: #Looping over and over again
  
# Here we use the If statement which evaluates a logical expression
# It is checking if the button is pressed by reading tha value of the pin
# If the button pin reads True (on), then it executes the indented code

if GPIO.input(Button_Pin) == False: #When the button is pressed, blink LED
  sleep(LED_Off) #Keep LED off for defined duration
  GPIO.output(LED_Pin, GPIO.HIGH) #Turn LED on
  sleep(LED_On) #Keep LED on for defined duration
  GPIO.output(LED_Pin, GPIO.LOW) #Turn lED off

# If the button is not pressed, the code will go to the else statement
else:
  print('Button not pressed')
  sleep(1)
