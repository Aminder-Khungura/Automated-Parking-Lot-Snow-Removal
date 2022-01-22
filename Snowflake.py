import pygame
import HARD_CODED_VALUES as HCV
import Barriers


class Snowflake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.character = pygame.image.load('snowflake.png').convert_alpha()
        self.character = pygame.transform.scale(self.character, (HCV.X_TRANSFORM, HCV.Y_TRANSFORM))
        self.possible_coors = [[0] * 2] * (HCV.GRID_ROWS * HCV.GRID_COLS)
        self.possible_coors = self.get_possible_coors()
        self.pix_x = 0
        self.pix_y = 0
        self.barriers = Barriers.Barriers(self.parent_screen)
        self.parkinglot_coors = self.get_parkinglot_coors()
        self.snowflake_coors = self.parkinglot_coors[:]

    def get_possible_coors(self):
        array_index = 0
        for i in range(HCV.GRID_COLS):
            for j in range(HCV.GRID_ROWS):
                self.possible_coors[array_index] = [j, i]
                array_index += 1
        return self.possible_coors

    def get_parkinglot_coors(self):
        self.parkinglot_coors = [[29, 1], [30, 1], [31, 1],
                            [27, 2], [28, 2], [29, 2], [30, 2], [31, 2], [32, 2],
                            [26, 3], [27, 3], [28, 3], [29, 3], [30, 3], [31, 3], [32, 3], [33, 3],
                            [25, 4], [26, 4], [27, 4], [28, 4], [29, 4], [30, 4], [31, 4], [32, 4], [33, 4],
                            [23, 5], [24, 5], [25, 5], [26, 5], [27, 5], [28, 5], [29, 5], [30, 5], [31, 5], [32, 5], [33, 5], [34, 5],
                            [21, 6], [22, 6], [23, 6], [24, 6], [25, 6], [26, 6], [27, 6], [28, 6], [29, 6], [30, 6], [31, 6], [32, 6], [33, 6], [34, 6],
                            [20, 7], [21, 7], [22, 7], [23, 7], [24, 7], [25, 7], [26, 7], [27, 7], [28, 7], [29, 7], [30, 7], [31, 7], [32, 7], [33, 7], [34, 7], [35, 7],
                            [19, 8], [20, 8], [21, 8], [22, 8], [23, 8], [24, 8], [25, 8], [26, 8], [27, 8], [28, 8], [29, 8], [30, 8], [31, 8], [32, 8], [33, 8], [34, 8], [35, 8], [36, 8],
                            [17, 9], [18, 9], [19, 9], [20, 9], [21, 9], [22, 9], [23, 9], [24, 9], [25, 9], [26, 9], [27, 9], [28, 9], [29, 9], [30, 9], [31, 9], [32, 9], [33, 9], [34, 9], [35, 9], [36, 9],
                            [15, 10], [16, 10], [17, 10], [18, 10], [19, 10], [20, 10], [21, 10], [22, 10], [23, 10], [24, 10], [25, 10], [26, 10], [27, 10], [28, 10], [29, 10], [30, 10], [31, 10], [32, 10], [33, 10], [34, 10], [35, 10], [36, 10], [37, 10],
                            [13, 11], [14, 11], [15, 11], [16, 11], [17, 11], [18, 11], [19, 11], [20, 11], [21, 11], [22, 11], [23, 11], [24, 11], [25, 11], [26, 11], [27, 11], [28, 11], [29, 11], [30, 11], [31, 11], [32, 11], [33, 11], [34, 11], [35, 11], [36, 11], [37, 11],
                            [12, 12], [13, 12], [14, 12], [15, 12], [16, 12], [17, 12], [18, 12], [19, 12], [20, 12], [21, 12], [22, 12], [23, 12], [24, 12], [25, 12], [26, 12], [27, 12], [28, 12], [29, 12], [30, 12], [31, 12], [32, 12], [33, 12], [34, 12], [35, 12], [36, 12], [37, 12],
                            [11, 13], [12, 13], [13, 13], [14, 13], [15, 13], [16, 13], [17, 13], [18, 13], [19, 13], [20, 13], [21, 13], [22, 13], [23, 13], [24, 13], [25, 13], [26, 13], [27, 13], [28, 13], [29, 13], [30, 13], [31, 13], [32, 13], [33, 13], [34, 13], [35, 13],
                            [9, 14], [10, 14], [11, 14], [12, 14], [13, 14], [14, 14], [15, 14], [16, 14], [17, 14], [18, 14], [19, 14], [20, 14], [21, 14], [22, 14], [23, 14], [24, 14], [25, 14], [26, 14], [27, 14], [31, 14],
                            [8, 15], [9, 15], [10, 15], [11, 15], [12, 15], [13, 15], [14, 15], [15, 15], [16, 15], [17, 15], [18, 15], [19, 15], [20, 15], [21, 15], [22, 15], [23, 15], [24, 15], [25, 15],
                            [8, 16], [9, 16], [10, 16], [11, 16], [12, 16], [13, 16], [14, 16], [15, 16], [16, 16], [17, 16], [18, 16], [19, 16], [20, 16], [21, 16], [22, 16], [23, 16], [24, 16],
                            [8, 17], [9, 17], [10, 17], [11, 17], [12, 17], [13, 17], [14, 17], [15, 17], [16, 17], [17, 17], [18, 17], [19, 17], [20, 17], [21, 17], [22, 17], [23, 17], [23, 17],
                            [9, 18], [10, 18], [11, 18], [12, 18], [13, 18], [14, 18], [15, 18], [16, 18], [17, 18], [18, 18], [19, 18], [20, 18], [21, 18],
                            [10, 19], [11, 19], [12, 19], [13, 19], [14, 19], [15, 19], [16, 19], [17, 19], [18, 19], [19, 19], [20, 19],
                            [10, 20], [11, 20], [12, 20], [13, 20], [14, 20], [15, 20], [16, 20], [17, 20], [18, 20],
                            [11, 21], [12, 21], [13, 21], [14, 21], [15, 21], [16, 21], [17, 21],
                            [12, 22], [13, 22], [14, 22], [15, 22],
                            [13, 23], [14, 23],
                            [34, 34],
                            [32, 35], [33, 35], [34, 35], [35, 35], [36, 35], [37, 35], [38, 35], [39, 35],
                            [31, 36], [32, 36], [33, 36], [34, 36], [35, 36], [36, 36], [37, 36], [38, 36], [39, 36], [40, 36],
                            [29, 37], [30, 37], [31, 37], [32, 37], [33, 37], [34, 37], [35, 37], [36, 37], [37, 37], [38, 37], [39, 37], [40, 37], [41, 37],
                            [28, 38], [29, 38], [30, 38], [31, 38], [32, 38], [33, 38], [34, 38], [35, 38], [36, 38], [37, 38], [38, 38], [39, 38], [40, 38], [41, 38],
                            [26, 39], [27, 39], [28, 39], [29, 39], [30, 39], [31, 39], [32, 39], [33, 39], [34, 39], [35, 39], [36, 39], [37, 39], [38, 39], [39, 39], [40, 39],
                            [25, 40], [26, 40], [27, 40], [28, 40], [29, 40], [30, 40], [31, 40], [32, 40], [33, 40], [34, 40], [35, 40], [36, 40], [37, 40], [38, 40], [39, 40],
                            [24, 41], [25, 41], [26, 41], [27, 41], [28, 41], [29, 41], [30, 41], [31, 41], [32, 41], [33, 41], [34, 41], [35, 41], [36, 41], [37, 41],
                            [24, 42], [25, 42], [26, 42], [27, 42], [28, 42], [29, 42], [30, 42], [31, 42], [32, 42], [33, 42], [34, 42], [35, 42], [36, 42],
                            [25, 43], [26, 43], [27, 43], [28, 43], [29, 43], [30, 43], [31, 43], [32, 43], [33, 43], [34, 43],
                            [26, 44], [27, 44], [28, 44], [29, 44], [30, 44], [31, 44], [32, 44], [33, 44],
                            [27, 45], [28, 45], [29, 45], [30, 45], [31, 45],
                            [27, 46], [28, 46], [29, 46],
                            [28, 47]]

        # Remove coordinates from self.parkinglot_coors that are on boundary coordinates
        for i in self.barriers.grid_boundary_coors_INT:
            coor = list(i)
            if coor in self.parkinglot_coors:
                self.parkinglot_coors.remove(coor)

        return self.parkinglot_coors

    def draw(self):
        for i in self.snowflake_coors:
            coor = i
            # Convert grid coordinates to pixel coordinates
            self.pix_x = coor[0] * HCV.BLOCK_WIDTH
            self.pix_y = coor[1] * HCV.BLOCK_WIDTH
            self.parent_screen.blit(self.character, [self.pix_x, self.pix_y])