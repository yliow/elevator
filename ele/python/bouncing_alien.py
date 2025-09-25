import sys, pygame

# Initialize Pygame
pygame.init()

# Set drawing surface to 680x480
WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)
surface = pygame.display.set_mode(SIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Set speed of alien to [1,2]
XSPEED = 1
YSPEED = 2
speed = [XSPEED, YSPEED]

# Load sound
tag = pygame.mixer.Sound("ChatTag.wav")

while 1:

    # Exit if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    

    # Draw surface
    surface.fill(BLACK)
    pygame.display.flip()
