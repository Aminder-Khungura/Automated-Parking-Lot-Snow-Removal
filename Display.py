import pygame
import HARD_CODED_VALUES as HCV
import Snowplow
import Snowflake
import Barriers


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((HCV.SCREEN_WIDTH, HCV.SCREEN_HEIGHT))
        pygame.display.set_caption("Snowplow Visualization")
        self.icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(self.icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow.Snowplow(self.screen)
        self.snowflake = Snowflake.Snowflake(self.screen)
        self.barriers = Barriers.Barriers(self.screen)
        self.collision = False

    def draw_background(self):
        self.screen.blit(self.background_image, [0, 0])

    def draw_grid(self):
        for i in range(HCV.GRID_ROWS):
            pygame.draw.line(self.screen, HCV.WHITE, (i * HCV.BLOCK_WIDTH, 0), (i * HCV.BLOCK_WIDTH, HCV.SCREEN_WIDTH))
        for i in range(HCV.GRID_COLS):
            pygame.draw.line(self.screen, HCV.WHITE, (0, i * HCV.BLOCK_HEIGHT), (HCV.SCREEN_HEIGHT, i * HCV.BLOCK_HEIGHT))

    def detect_collision(self, x, y):
        coor = str(x) + ' ' + str(y)
        if coor in self.barriers.grid_boundary_coors:
            print('On Boundary')
            self.collision = True
            print('Collision')
        elif coor in self.barriers.grid_parkingspot_coors:
            print('On Parkingspot')
        elif coor in self.barriers.grid_entry_coors:
            print('On Entry')
        else:
            print('On Black')
        return self.collision

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                # Place snowplow at start location
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.snowplow.get_start_pos()
                    self.draw_background()
                    self.snowplow.draw_snowplow(self.snowplow.x_start, self.snowplow.y_start)

                # Move snowplow
                if event.type == pygame.KEYDOWN:
                    pix_x, pix_y, grid_x, grid_y, original_x_coor, original_y_coor = self.snowplow.move_snowplow(event)
                    collision_detected = self.detect_collision(grid_x, grid_y)
                    if not collision_detected:
                        self.draw_background()
                        self.snowplow.draw_snowplow(pix_x, pix_y)
                    else:
                        self.snowplow.x_coor = original_x_coor
                        self.snowplow.y_coor = original_y_coor
                        self.collision = False

                self.detect_collision(self.snowplow.grid_x_coor, self.snowplow.grid_y_coor)

                self.draw_grid()
                # Quit
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()