import pygame
import HARD_CODED_VALUES as HCV


class Snowpile:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.character = pygame.image.load('snowpile.png').convert_alpha()
        self.character = pygame.transform.scale(self.character, (HCV.Snowpile_X_TRANSFORM, HCV.Snowpile_Y_TRANSFORM))
        self.coors = []

    def add_coor(self, x, y):
        coor = [x, y]
        self.coors.append(coor)

    def draw(self):
        for i in self.coors:
            coor = i
            # Convert grid coordinates to pixel coordinates
            pix_x = coor[0] * HCV.BLOCK_WIDTH
            pix_y = coor[1] * HCV.BLOCK_WIDTH
            self.parent_screen.blit(self.character, [pix_x, pix_y])