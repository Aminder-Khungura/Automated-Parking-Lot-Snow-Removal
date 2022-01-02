# Use pygame for visualization, need to see:
# 1) The movement of snow plow
# 2) When plow is down and up
# 3) Use color gradient show where snow is being pilled up

import pygame
import cv2 as cv
import pandas as pd
import numpy as np


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow_character.png')

    def place_snowplow(self, x, y):
        self.parent_screen.blit(self.snowplow_character, [x, y])
        pygame.display.flip()


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((987, 964))
        pygame.display.set_caption("Snowplow Visualization")
        self.icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(self.icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_coor, y_coor = pygame.mouse.get_pos()
                    x_coor -= 30
                    y_coor -= 30
                    self.screen.blit(self.background_image, [0, 0])
                    self.snowplow.place_snowplow(x_coor, y_coor)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        y_coor += 10
                    if event.key == pygame.K_UP:
                        y_coor -= 10
                    if event.key == pygame.K_LEFT:
                        x_coor -= 10
                    if event.key == pygame.K_RIGHT:
                        x_coor += 10
                    self.screen.blit(self.background_image, [0, 0])
                    self.snowplow.place_snowplow(x_coor, y_coor)
            pygame.display.flip()


if __name__ == '__main__':
    display = Display()
    display.run()
