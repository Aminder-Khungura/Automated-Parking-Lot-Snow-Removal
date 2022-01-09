import pygame
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