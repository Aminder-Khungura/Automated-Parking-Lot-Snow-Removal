import pygame
import HARD_CODED_VALUES as HCV


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
        self.pix_y = grid_y * HCV.BLOCK_WIDTH
        self.parent_screen.blit(self.snowflake_character, [self.pix_x, self.pix_y])
        pygame.display.flip()

