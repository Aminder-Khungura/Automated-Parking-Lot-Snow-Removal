# Use pygame for visualization, need to see:
# 1) The movement of snow plow
# 2) When plow is down and up
# 3) Use color gradient show where snow is being pilled up

import pygame
import cv2 as cv
import numpy as np
import hard_coded_values as HCV


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow_character.png')

    @staticmethod
    def get_click_pos():
        x_coor, y_coor = pygame.mouse.get_pos()
        x_coor -= HCV.snowplow_img_offset
        y_coor -= HCV.snowplow_img_offset
        return x_coor, y_coor

    def draw_snowplow(self, x, y):
        self.parent_screen.blit(self.snowplow_character, [x, y])
        pygame.display.flip()

    def pacman_algorithm(self):
        self.running = True
        # create algorithm that controls snowplow's movement to maximize the amount of snow collected
        # add small snowflake images to background that will be collected by snowplow when position overlaps pics


class Snowflake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowflake = pygame.image.load('snowflake.png').convert()
        self.snowflake = pygame.transform.scale(self.snowflake, (HCV.x_transform, HCV.y_transform))
        self.parent_screen.blit(self.snowflake, [0, 0])

    def draw_snowflake(self, pos):
        self.grid_pos = pos
        self.pix_pos


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((HCV.screen_width, HCV.screen_height))
        pygame.display.set_caption("Snowplow Visualization")
        self.icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(self.icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow(self.screen)
        self.gridblock_width = HCV.screen_width // HCV.pixels_per_block
        self.gridblock_height = HCV.screen_height // HCV.pixels_per_block
        self.snowflake = Snowflake(self.screen)

    def get_barrier_coordinates(self, loop_counter):
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

            y_boundary, x_boundary = np.where(np.all(boundary_closing != HCV.black, axis=2))
            y_parkingspot, x_parkingspot = np.where(np.all(parkingspot_closing != HCV.black, axis=2))
            y_entry, x_entry = np.where(np.all(entry_closing != HCV.black, axis=2))

    def draw_grid(self):
        for i in range(HCV.screen_width // self.gridblock_width):
            pygame.draw.line(self.screen, HCV.white, (i * self.gridblock_width, 0), (i * self.gridblock_width, HCV.screen_width))

        for i in range(HCV.screen_height // self.gridblock_height):
            pygame.draw.line(self.screen, HCV.white, (0, i * self.gridblock_height), (HCV.screen_height, i * self.gridblock_height))

    def run(self):
        running = True
        loop_counter = 1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_coor, y_coor = self.snowplow.get_click_pos()
                    self.screen.blit(self.background_image, [0, 0])
                    self.snowplow.draw_snowplow(x_coor, y_coor)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        y_coor += HCV.move
                    if event.key == pygame.K_UP:
                        y_coor -= HCV.move
                    if event.key == pygame.K_LEFT:
                        x_coor -= HCV.move
                    if event.key == pygame.K_RIGHT:
                        x_coor += HCV.move
                    self.screen.blit(self.background_image, [0, 0])
                    self.snowplow.draw_snowplow(x_coor, y_coor)

                self.get_barrier_coordinates(loop_counter)
                self.draw_grid()
                loop_counter += 1
            pygame.display.flip()


if __name__ == '__main__':
    display = Display()
    display.run()
