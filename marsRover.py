#https://www.jpl.nasa.gov/edu/learn/project/code-a-mars-rover-driving-game/
#https://realpython.com/pygame-a-primer/

import pygame as pg #Import the pygame module
import random #import random numbers

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import *

#set variables for width & height
width = 600
height = 350

#define function to get random spawn coordinates
def spawn_random():
    spawn_x = random.randint(0, width)
    spawn_y = random.randint(0, height)
    return spawn_x, spawn_y

#define generic class for gameobject
'''class GameObject:

    def __init__(self, image_path, x, y, width, height):
        #Player image import and resize
        object_image = pg.image.load(image_path)
        self.image = pg.transform.scale(object_image, (width, height))

        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    #Draw the object by blitting it onto the background (screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))
'''

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pg.image.load(r"C:\Users\carlittle\Documents\rover\venv\Lib\rover5050.png").convert_alpha() #load player image as surface
        #The RLEACCEL constant is an optional parameter that helps pygame render more quickly on non-accelerated displays
        self.surf.set_colorkey((255,255,255),RLEACCEL)  #Set the current color key for the player surface on RLEACCEL non accelerated surface
        self.rect = self.surf.get_rect()


    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pg.image.load(r"C:\Users\carlittle\Documents\rover\venv\Lib\meteor_50x35.1.png").convert_alpha()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        #starting position & speed are randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(width + 20, width + 100),
                random.randint(0, height),
            )
        )
        self.speed = random.randint(2,10) #set enemy speed as random number between a & b

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the destination object
class Destination(pg.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, xy_spawn):
       # Call the parent class (Sprite) constructor
       pg.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.surf = pg.image.load(
           r"C:\Users\carlittle\Documents\rover\venv\checkered-flag.png").convert_alpha()  # load player image as surface
       self.surf.set_colorkey((255, 255, 255),RLEACCEL)  # Set the current color key for the player surface on RLEACCEL non accelerated surface
       self.x, self.y = xy_spawn #set rand coordinates
       self.rect = self.surf.get_rect(center=(self.x, self.y)) #spawn center at rand coordinates

#GAME SETUP
pg.init() # Initialize the pygame library
screen = pg.display.set_mode((width, height),pg.RESIZABLE) # Create the screen object
pg.display.set_caption("Mars Rover") # Add title to display window

# Create a custom event for adding a new enemy
ADDENEMY = pg.USEREVENT + 1
pg.time.set_timer(ADDENEMY, 1000)

player = Player() # Create player
dest = Destination(spawn_random()) # Create destination

# Create groups to hold enemy sprites and all sprites
enemies = pg.sprite.Group() # - enemies is used for collision detection and position updates

all_sprites = pg.sprite.Group() # - all_sprites is used for rendering
all_sprites.add(player)

objects = pg.sprite.Group() # - objects is used for collision detection and position updates
objects.add(dest)

#Setup the clock for decent framerate
clock = pg.time.Clock()

#status variables to keep the main loop running
running = True # variable to continue or end game
dest_achieved = False # variable to respawn destination
score = 0 # variable to keep score

#MAIN loop
while running:
    #look for event in the queue
    for event in pg.event.get():
        #did user press a key?
        if event.type == KEYDOWN:
            #was ESC key pressed?
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button?
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new destination?
        if dest_achieved == True:
            #Create the new dest and add it to oject groups
            dest = Destination(spawn_random())
            objects.add(dest)
            score = score + 1 #increment score
            dest_achieved = False #reset achievement variable


    # Get all the keys currently pressed and check for user input
    pressed_keys = pg.key.get_pressed()
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    # create background surface
    terrain = pg.image.load(
        r"C:\Users\carlittle\Documents\rover\venv\Lib\scratchrover_backgrounds_mars\terrain.jpg").convert() #load image
    background = pg.transform.scale(terrain, (screen.get_width(), screen.get_height())) #set image as background same size as screen
    screen.blit(background, (0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw all objects
    for entity in objects:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pg.sprite.spritecollideany(player, enemies):
        #If so, then remove the player and stop the loop
        player.kill()
        running = False

    # Check if player has reached destination
    if pg.sprite.spritecollide(player, objects, 0):
        dest.kill() # remove current destination
        dest_achieved = True # set achievement to trigger respawn
        running = True # continue game

    # Flip the display
    pg.display.flip()

    #Ensure program maintains a rate of 30 frames per second
    clock.tick(30)


# Done! Time to quit
pg.quit() #close window
print("GAME OVER! Your score: "+str(score)) #print score