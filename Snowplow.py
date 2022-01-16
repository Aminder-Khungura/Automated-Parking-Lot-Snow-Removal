import pygame
import HARD_CODED_VALUES as HCV
import Stats


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow_character.png')
        self.snowplow_character = pygame.transform.scale(self.snowplow_character, (HCV.SP_X_TRANSFORM, HCV.SP_Y_TRANSFORM))
        self.x_start = 0
        self.y_start = 0
        self.x_coor = 0
        self.y_coor = 0
        self.grid_x_start = 0
        self.grid_y_start = 0
        self.grid_x_coor = 0
        self.grid_y_coor = 0
        self.stats = Stats.Stats(self.parent_screen)
        self.start_pos_set = False

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
        self.start_pos_set = True

    def draw_snowplow(self, x, y):
        self.parent_screen.blit(self.snowplow_character, [x, y])

    def move_snowplow(self, event):
        original_x_coor = self.x_coor
        original_y_coor = self.y_coor
        if event.key == pygame.K_DOWN:
            self.y_coor += HCV.MOVE_Y
            self.grid_y_coor = (self.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
        if event.key == pygame.K_UP:
            self.y_coor -= HCV.MOVE_Y
            self.grid_y_coor = (self.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
        if event.key == pygame.K_LEFT:
            self.x_coor -= HCV.MOVE_X
            self.grid_x_coor = (self.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        if event.key == pygame.K_RIGHT:
            self.x_coor += HCV.MOVE_X
            self.grid_x_coor = (self.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        return self.x_coor, self.y_coor, self.grid_x_coor, self.grid_y_coor, original_x_coor, original_y_coor
