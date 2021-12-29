# Use pygame for visualization, need to see:
# 1) The movement of snow plow
# 2) When plow is down and up
# 3) Use color gradient show where snow is being pilled up

import pygame

# Initialize game
pygame.init()

# Customize screen
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Snow Plow")
icon = pygame.image.load('snowplow.png')
pygame.display.set_icon(icon)
background_image = pygame.image.load('Edited Parking Lot.jpg').convert()


def background():
    screen.blit(background_image, [0, 0])


# Snowplow character
snowplow_character = pygame.image.load('snowplow_character.png')


def snowplow():
    x = 100
    y = 100
    screen.blit(snowplow_character, [x, y])


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Set background and add snowplow character
    background()
    snowplow()
    pygame.display.flip()