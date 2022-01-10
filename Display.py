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

    def draw_background(self):
        self.screen.blit(self.background_image, [0, 0])

    def draw_grid(self):
        for i in range(HCV.GRID_ROWS):
            pygame.draw.line(self.screen, HCV.WHITE, (i * HCV.BLOCK_WIDTH, 0), (i * HCV.BLOCK_WIDTH, HCV.SCREEN_WIDTH))
        for i in range(HCV.GRID_COLS):
            pygame.draw.line(self.screen, HCV.WHITE, (0, i * HCV.BLOCK_HEIGHT), (HCV.SCREEN_HEIGHT, i * HCV.BLOCK_HEIGHT))

    def check_if_on_boundary(self, x, y):
        coor = str(x) + ' ' + str(y)
        if coor in self.barriers.grid_boundary_coors:
            print('On Boundary: ', coor)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Place snowplow at user's start location
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.snowplow.get_start_pos()
                    self.draw_background()
                    self.snowplow.draw_snowplow(self.snowplow.x_start, self.snowplow.y_start)

                # Move snowplow with arrow keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.snowplow.y_coor += HCV.MOVE_Y
                        self.snowplow.grid_y_coor = (self.snowplow.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
                    if event.key == pygame.K_UP:
                        self.snowplow.y_coor -= HCV.MOVE_Y
                        self.snowplow.grid_y_coor = (self.snowplow.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
                    if event.key == pygame.K_LEFT:
                        self.snowplow.x_coor -= HCV.MOVE_X
                        self.snowplow.grid_x_coor = (self.snowplow.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
                    if event.key == pygame.K_RIGHT:
                        self.snowplow.x_coor += HCV.MOVE_X
                        self.snowplow.grid_x_coor = (self.snowplow.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
                    self.draw_background()
                    self.snowplow.draw_snowplow(self.snowplow.x_coor, self.snowplow.y_coor)

                self.snowflake.draw_snowflake(30, 0)
                self.draw_grid()
                self.check_if_on_boundary(self.snowplow.grid_x_coor, self.snowplow.grid_y_coor)
            pygame.display.flip()