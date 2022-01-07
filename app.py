# Use pygame for visualization, need to see:
# 1) The movement of snow plow
# 2) When plow is down and up
# 3) Use color gradient show where snow is being pilled up

import pygame
import cv2 as cv
import numpy as np


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow_character.png')

    def place_snowplow(self, x, y):
        self.parent_screen.blit(self.snowplow_character, [x, y])
        pygame.display.flip()

    def pacman_algorithm(self):
        self.running = True
        # create algorithm that controls snowplow's movement to maximize the amount of snow collected
        # add small snowflake images to background that will be collected by snowplow when position overlaps pics
class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("Snowplow Visualization")
        self.icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(self.icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow(self.screen)

    def parkinglot_barriers(self, loop_counter):
        # Convert windowSurface to cv2 Reference: https://stackoverflow.com/questions/19240422/display-cv2-videocapture-image-inside-pygame-surface
        view = pygame.surfarray.array3d(self.screen)
        # Convert from (width, height, channel) to (height, width, channel)
        view = view.transpose([1, 0, 2])
        if loop_counter == 1:
            img_hsv = cv.cvtColor(view, cv.COLOR_BGR2HSV)

            # Define color ranges for masks
            lower_green = np.array([50, 100, 100])
            upper_green = np.array([70, 255, 255])
            lower_blue = np.array([0, 100, 100])
            upper_blue = np.array([10, 255, 255])
            lower_red = np.array([110, 100, 100])
            upper_red = np.array([130, 255, 255])

            # create masks for boundary, parking spots, and entry
            boundary_mask = cv.inRange(img_hsv, lower_blue, upper_blue)
            parkingspot_mask = cv.inRange(img_hsv, lower_red, upper_red)
            entry_mask = cv.inRange(img_hsv, lower_green, upper_green)

            # Use mask to extract the area of interest
            boundary_result = cv.bitwise_and(img_hsv, img_hsv, mask=boundary_mask)
            parkingspot_result = cv.bitwise_and(img_hsv, img_hsv, mask=parkingspot_mask)
            entry_result = cv.bitwise_and(img_hsv, img_hsv, mask=entry_mask)

            kernel_erode = np.ones((2, 2), np.uint8)
            kernel_close = np.ones((15, 15), np.uint8)

            boundary_erode = cv.erode(boundary_result, np.ones((1, 1), np.uint8))
            boundary_closing = cv.morphologyEx(boundary_erode, cv.MORPH_CLOSE, kernel_close)

            parkingspot_erode = cv.erode(parkingspot_result, kernel_erode)
            parkingspot_closing = cv.morphologyEx(parkingspot_erode, cv.MORPH_CLOSE, kernel_close)

            entry_erode = cv.erode(entry_result, kernel_erode)
            entry_closing = cv.morphologyEx(entry_erode, cv.MORPH_CLOSE, kernel_close)

            y_boundary, x_boundary = np.where(np.all(boundary_closing != [0, 0, 0], axis=2))
            y_parkingspot, x_parkingspot = np.where(np.all(parkingspot_closing != [0, 0, 0], axis=2))
            y_entry, x_entry = np.where(np.all(entry_closing != [0, 0, 0], axis=2))

    def run(self):
        running = True
        loop_counter = 1
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

                self.parkinglot_barriers(loop_counter)
                loop_counter += 1
            pygame.display.flip()


if __name__ == '__main__':
    display = Display()
    display.run()
