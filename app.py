import pygame
import cv2 as cv
import numpy as np
import HARD_CODED_VALUES as HCV


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow_character.png')
        self.snowplow_character = pygame.transform.scale(self.snowplow_character, (45, 45))
        self.x_start = 0
        self.y_start = 0
        self.x_coor = 0
        self.y_coor = 0
        self.grid_x_start = 0
        self.grid_y_start = 0
        self.grid_x_coor = 0
        self.grid_y_coor = 0

    # Store the pixel and grid coordinates of the snowplow starting location
    def get_start_pos(self):
        self.x_coor, self.y_coor = pygame.mouse.get_pos()
        self.x_coor -= HCV.SNOWPLOW_IMG_OFFSET
        self.y_coor -= HCV.SNOWPLOW_IMG_OFFSET
        self.x_start = self.x_coor
        self.y_start = self.y_coor
        self.grid_x_start = (self.x_start + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        self.grid_y_start = (self.y_start + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
        self.grid_x_coor = (self.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        self.grid_y_coor = (self.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT

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
        self.snowflake_character = pygame.image.load('snowflake.png').convert()
        self.snowflake_character = pygame.transform.scale(self.snowflake_character, (HCV.X_TRANSFORM, HCV.Y_TRANSFORM))
        self.pix_x = 0
        self.pix_y = 0

    def draw_snowflake(self, grid_x, grid_y):
        # Convert grid coordinates to pixel coordinates
        self.pix_x = grid_x * HCV.BLOCK_WIDTH
        self.pix_y = grid_y * HCV.BLOCK_HEIGHT
        self.parent_screen.blit(self.snowflake_character, [self.pix_x, self.pix_y])
        pygame.display.flip()


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((HCV.SCREEN_WIDTH, HCV.SCREEN_HEIGHT))
        pygame.display.set_caption("Snowplow Visualization")
        self.icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(self.icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow(self.screen)
        self.snowflake = Snowflake(self.screen)

    def draw_background(self):
        self.screen.blit(self.background_image, [0, 0])

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

            y_boundary, x_boundary = np.where(np.all(boundary_closing != HCV.BLACK, axis=2))
            y_parkingspot, x_parkingspot = np.where(np.all(parkingspot_closing != HCV.BLACK, axis=2))
            y_entry, x_entry = np.where(np.all(entry_closing != HCV.BLACK, axis=2))

    def draw_grid(self):
        for i in range(HCV.GRID_COLS):
            pygame.draw.line(self.screen, HCV.WHITE, (i * HCV.BLOCK_WIDTH, 0), (i * HCV.BLOCK_WIDTH, HCV.SCREEN_WIDTH))

        for i in range(HCV.GRID_ROWS):
            pygame.draw.line(self.screen, HCV.WHITE, (0, i * HCV.BLOCK_HEIGHT), (HCV.SCREEN_HEIGHT, i * HCV.BLOCK_HEIGHT))

    def run(self):
        running = True
        loop_counter = 1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.snowplow.get_start_pos()
                    self.draw_background()
                    self.snowplow.draw_snowplow(self.snowplow.x_start, self.snowplow.y_start)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.snowplow.y_coor += HCV.MOVE_Y
                        self.snowplow.grid_y_coor = (self.snowplow.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
                    if event.key == pygame.K_UP:
                        self.snowplow.y_coor -= HCV.MOVE_Y
                        self.snowplow.grid_y_coor = (self.snowplow.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
                    if event.key == pygame.K_LEFT:
                        self.snowplow.x_coor -= HCV.MOVE_X
                        self.snowplow.grid_x_coor = (self.snowplow.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
                    if event.key == pygame.K_RIGHT:
                        self.snowplow.x_coor += HCV.MOVE_X
                        self.snowplow.grid_x_coor = (self.snowplow.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
                    self.draw_background()
                    self.snowplow.draw_snowplow(self.snowplow.x_coor, self.snowplow.y_coor)
                self.get_barrier_coordinates(loop_counter)
                self.snowflake.draw_snowflake(5, 3)
                self.draw_grid()
                loop_counter += 1
            pygame.display.flip()


if __name__ == '__main__':
    display = Display()
    display.run()
