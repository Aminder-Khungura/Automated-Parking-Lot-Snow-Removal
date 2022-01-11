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
        self.barriers = Barriers.Barriers(self.parent_screen)

    def get_possible_coors(self, parent_screen):
        array_index = 0
        for i in range(HCV.GRID_COLS):
            for j in range(HCV.GRID_ROWS):
                self.possible_coors[array_index] = [j, i]
                array_index += 1
        return self.possible_coors

    def check_coors(self, parent_screen):
        on_boundary = False
        parkinglot_coors = [[]]
        i = 0
        # Starting checking each grid block from [0, 0] to [49, 49]
        while i <= len(self.possible_coors):
            coor = self.possible_coors[i]

            # Selected grid block on top of boundary
            if coor in self.barriers.grid_boundary_coors or coor in self.barriers.grid_entry_coors:
                on_boundary = True
                while on_boundary:
                    parkinglot_coors.append(coor)
                    i += 1
                    coor = self.possible_coors[i]

                    # Check if grid block entered parking lot
                    if coor not in self.barriers.grid_boundary_coors or coor not in self.barriers.grid_entry_coors:
                        on_boundary = False
                        inside_parkinglot = True
                        entered_row = coor[1]

                # Selected grid block is inside parking lot
                while inside_parkinglot:
                    parkinglot_coors.append(coor)
                    i += 1
                    coor = self.possible_coors[i]
                    current_row = coor[1]

                    # Check if grid block exiting parking lot
                    if (coor in self.barriers.grid_boundary_coors or coor in self.barriers.grid_entry_coors) and :
                        on_boundary = False
                        inside_parkinglot = True










        # Convert grid coordinates to pixel coordinates
        # self.pix_x = x * HCV.BLOCK_WIDTH
        # self.pix_y = y * HCV.BLOCK_WIDTH
        # self.parent_screen.blit(self.snowflake_character, [self.pix_x, self.pix_y])

