import pygame
import HARD_CODED_VALUES as HCV
import Snowplow
import Snowflake
import Snowpile
import Barriers
import Stats


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((HCV.SCREEN_WIDTH, HCV.SCREEN_HEIGHT))
        pygame.display.set_caption("Parking Lot Snow Removal Visualization")
        self.icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(self.icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow.Snowplow(self.screen)
        self.snowflake = Snowflake.Snowflake(self.screen)
        self.snowpile = Snowpile.Snowpile(self.screen)
        self.barriers = Barriers.Barriers(self.screen)
        self.collision = False
        self.stats = Stats.Stats(self.screen)
        self.font = pygame.font.SysFont('Corbel', 32)

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
            self.collision = True
        else:
            self.collision = False
        return self.collision

    def remove_snow(self, x, y):
        coor = [x, y]
        if coor in self.snowflake.snowflake_coors:
            self.snowflake.snowflake_coors.remove(coor)
            self.stats.amount_of_snow_held += 1
        return self.snowflake.snowflake_coors

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    running = False

                # Place snowplow at start location
                if event.type == pygame.MOUSEBUTTONDOWN and not self.snowplow.start_pos_set:
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
                        self.stats.distance_travelled += 1
                    else:
                        self.draw_background()
                        self.snowplow.draw_snowplow(pix_x, pix_y)
                        self.snowpile.update_snowpile_coors(grid_x, grid_y)
                        self.stats.collisions += 1
                        self.stats.points += self.stats.amount_of_snow_held

                self.snowflake.snowflake_coors = self.remove_snow(self.snowplow.grid_x_coor, self.snowplow.grid_y_coor)
                self.snowflake.draw_snowflakes(self.snowflake.snowflake_coors)
                self.stats.snowpiles = len(self.snowpile.snowpile_coors)
                self.snowpile.draw_snowpiles(self.snowpile.snowpile_coors)
                self.stats.display_info(self.font)
                # self.draw_grid()

            pygame.display.update()