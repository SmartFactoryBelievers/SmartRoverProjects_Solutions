# Project 08

# Trying out the Pi Camera and learning about the different image settings

# Build the the Project 8 circuit and experiment with the camera in cool ways

#Challenge 1
# Try changing the camera resolution to the minimum with 64, 64 and see how it looks

#Challenge 2
# Try changing the camera resolution the maximum with 2592, 1944 and
# the framerate to 15 and see how it looks

#Challege 3
# Try changing the camera rotation to flip it upside down (0) or left or right (90, 270)

#Challenge 4
# Try adding a text on top of the image and changing the colors and size

#Challenge 5
# Try looping through all the contrast and brightness options
# and annotate the image with their current levels

#Challenge 6
# Try looping through all the IMAGE_EFFECTS, EXPOSURE_MODES, and AWB_MODES options
# and annotate the image with their current levels

#Importing libraries
# Here we want sleep for timing and picamera for the Pi's camera
from picamera import PiCamera, Color
from time import sleep

# Setting up the camera
camera = PiCamera()

# Change the number of pixels and clarity of the camera
# For challenge 1 and 2, see what low and high resolution look like
camera.resolution = (2592, 1944)

# Change the rate at which the camera records images
camera.framerate = 15

# Rotate the image by x degrees
# Note that the camera assembly is upside down so 180 is right side up
# For challenge 3, try other rotation angles
camera.rotation = 270

# For challenge 4, try annotating the image
# Add text on top of the image
camera.annotate_text = 'Hello World!'
# Change the text size on top of the image between 6 and 160
camera.annotate_text_size = 50
# Change the text color in front and back
camera.annotate_foreground = Color('red')
camera.annotate_background = Color('blue')

# Change the contrast between 0 and 100 (color/luminence difference between objects)
camera.contrast = 75

# Change the brightness of the image between 0 and 100
camera.brightness = 75

# Start the preview to view the camera image stream
camera.start_preview()
sleep(5)
camera.stop_preview()

# For challenge 5, try iterating through the brightness levels instead of contrast
camera.start_preview()
for i in range(100):
  camera.brightness = i
  camera.annotate_text = '%s' %i
  sleep(0.1)
camera.stop_preview()

# For challenge 6, try iterating through IMAGE_EFFECTS, EXPOSURE_MODES, and AWB_MODES

camera.start_preview()
for effect in camera.EXPOSURE_MODES:
  camera.annotate_text = '%s' %effect
  camera.exposure_mode = effect
  sleep(1)
camera.stop_preview()

camera.close()
