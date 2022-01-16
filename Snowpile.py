import pygame
import HARD_CODED_VALUES as HCV


class Snowpile:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowpile_character = pygame.image.load('snowpile.png').convert_alpha()
        self.snowpile_character = pygame.transform.scale(self.snowpile_character, (HCV.Snowpile_X_TRANSFORM, HCV.Snowpile_Y_TRANSFORM))
        self.snowpile_coors = []

    def update_snowpile_coors(self, x, y):
        coor = [x, y]
        self.snowpile_coors.append(coor)

    def draw_snowpiles(self, arr):
        for i in arr:
            coor = i
            # Convert grid coordinates to pixel coordinates
            pix_x = coor[0] * HCV.BLOCK_WIDTH
            pix_y = coor[1] * HCV.BLOCK_WIDTH
            self.parent_screen.blit(self.snowpile_character, [pix_x, pix_y])