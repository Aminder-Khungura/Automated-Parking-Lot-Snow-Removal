import pygame
import HARD_CODED_VALUES as HCV
import Barriers


class Snowflake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowflake_character = pygame.image.load('snowflake.png').convert()
        self.snowflake_character = pygame.transform.scale(self.snowflake_character, (HCV.X_TRANSFORM, HCV.Y_TRANSFORM))
        self.possible_coors = [[0] * 2] * (HCV.GRID_ROWS * HCV.GRID_COLS)
        self.possible_coors = self.get_possible_coors(self.parent_screen)
        self.pix_x = 0
        self.pix_y = 0
        # self.parkinglot_coors = [[]]
        self.barriers = Barriers.Barriers(self.parent_screen)

    def get_possible_coors(self, parent_screen):
        array_index = 0
        for i in range(HCV.GRID_COLS):
            for j in range(HCV.GRID_ROWS):
                self.possible_coors[array_index] = [j, i]
                array_index += 1
        return self.possible_coors

    # def get_parkinglot_coors(self):
    #     self.parkinglot_coors = [[]]
    #     on_boundary = False
    #     i = 0
    #     while i < len(self.possible_coors):
    #         coor = self.possible_coors[i]
    #         if coor in self.barriers.grid_boundary_coors:
    #             on_boundary = True
    #             parkinglot_coors.append(coor)
    #         while on_boundary:
    #             i += 1
    #             coor = self.possible_coors[i]
    #             if coor not in self.barriers.grid_boundary_coors:
    #                 on_boundary = False
    #                 parkinglot_coors.append(coor)
    #
    #         i += 1

    def draw_snowflakes(self, arr):
        for i in arr:
            coor = i
            # Convert grid coordinates to pixel coordinates
            self.pix_x = coor[0] * HCV.BLOCK_WIDTH
            self.pix_y = coor[1] * HCV.BLOCK_WIDTH
            self.parent_screen.blit(self.snowflake_character, [self.pix_x, self.pix_y])

