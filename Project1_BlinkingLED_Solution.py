# Project 1

# Learning to program and use outputs

# Build the the Project 1 circuit and blink a LED

#Challenge 1
# Try changing the LED_On and LED_Off variables to change the blinking pattern

#Challenge 2
# Replace the color LED with buzzer or white LED to try other outputs

#Importing libraries
# Libraries are defined sets of code for specific uses
# Here we want the sleep function for timing and GPIO for the Pi's pin
from time import sleep
import RPi.GPIO as GPIO

#Let's define variables so we can use them later
# Variables are words that take on values within the code
# This way, we can edit the value at the beginning and the changes flow through
LED_Pin = 40 #the internal Pi pin number that goes to snap 7

# For challenge 1, we can try different values here to blink in new patterns
LED_On = 3 #duration of LED flash, seconds
LED_Off = 1 #duration in between flashes, seconds

#Setting up our pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_Pin, GPIO.OUT, initial=GPIO.LOW) #Output pin, start off

while True: #Looping over and over again
  sleep(LED_Off) #Keep LED off for defined duration
  GPIO.output(LED_Pin, GPIO.HIGH) #Turn LED on
  sleep(LED_On) #Keep LED on for defined duration
  GPIO.output(LED_Pin, GPIO.LOW) #Turn lED off
 
print(list(f(10)))
