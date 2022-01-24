import pygame
import HARD_CODED_VALUES as HCV
import Snowplow
import Snowflake
import Snowpile
import Stats


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((HCV.SCREEN_WIDTH, HCV.SCREEN_HEIGHT))
        pygame.display.set_caption("Snow Removal Visualization")
        icon = pygame.image.load('snowplow.png')
        pygame.display.set_icon(icon)
        self.background_image = pygame.image.load('Edited Parking Lot.jpg').convert()
        self.screen.blit(self.background_image, [0, 0])
        self.snowplow = Snowplow.Snowplow(self.screen)
        self.snowflake = Snowflake.Snowflake(self.screen)
        self.snowpile = Snowpile.Snowpile(self.screen)
        self.stats = Stats.Stats(self.screen)
        self.font = pygame.font.SysFont('Corbel', 28)

    def draw_background(self):
        self.screen.blit(self.background_image, [0, 0])

    def draw_grid(self):
        for i in range(HCV.GRID_ROWS):
            pygame.draw.line(self.screen, HCV.WHITE, (i * HCV.BLOCK_WIDTH, 0), (i * HCV.BLOCK_WIDTH, HCV.SCREEN_WIDTH))
        for i in range(HCV.GRID_COLS):
            pygame.draw.line(self.screen, HCV.WHITE, (0, i * HCV.BLOCK_HEIGHT), (HCV.SCREEN_HEIGHT, i * HCV.BLOCK_HEIGHT))

    def remove_snow(self):
        coor = [self.snowplow.grid_x, self.snowplow.grid_y]
        if coor in self.snowflake.snowflake_coors:
            self.snowflake.snowflake_coors.remove(coor)
            self.stats.amount_removed += 1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                # Quit -----------------------------------------------------------------------------------------------
                if event.type == pygame.QUIT:
                    running = False

                # Place snowplow at start location -------------------------------------------------------------------
                if event.type == pygame.MOUSEBUTTONDOWN and not self.snowplow.start_pos_set:
                    self.snowplow.get_start_pos()
                    self.draw_background()
                    self.snowplow.draw()
                    self.remove_snow()

                # Move snowplow --------------------------------------------------------------------------------------
                if event.type == pygame.KEYDOWN:
                    self.snowplow.get_available_directions(self.snowplow.grid_x, self.snowplow.grid_y)
                    self.snowplow.snowflake_coors = self.snowflake.snowflake_coors
                    print('Coors:', self.snowplow.grid_x, self.snowplow.grid_y)
                    print('available_directions', self.snowplow.available_directions)
                    direction, num_of_moves, snow_found = self.snowplow.greedy_algorithm()
                    if snow_found:
                        for i in range(num_of_moves):
                            self.snowplow.greedy_movement(direction)
                            self.stats.distance_travelled += 1  # Update distance score
                            self.remove_snow()  # Update amount removed score
                            collision = self.snowplow.detect_collision(self.snowplow.grid_x, self.snowplow.grid_y)
                            if collision:
                                self.stats.collisions += 1  # Update collision score
                                # Create snowpile
                                if self.stats.amount_removed > 0:
                                    self.stats.total_removed += self.stats.amount_removed
                                    self.snowpile.add_coor(self.snowplow.grid_x, self.snowplow.grid_y)
                                    self.stats.amount_removed = 0
                                self.draw_background()
                                self.snowplow.draw()
                                self.snowplow.get_available_directions(self.snowplow.grid_x, self.snowplow.grid_y)
                            self.stats.snowpiles = len(self.snowpile.coors)  # Update snowpile score
                            # Update display
                            self.draw_background()
                            self.snowplow.draw()
                            self.snowflake.draw()
                            self.snowpile.draw()
                            self.stats.display_info(self.font)
                    else:
                        num_of_moves = self.snowplow.reposition()
                        self.stats.distance_travelled += num_of_moves  # Update distance score
                        self.remove_snow()  # Update amount removed score
                        collision = self.snowplow.detect_collision(self.snowplow.grid_x, self.snowplow.grid_y)
                        if collision:
                            self.stats.collisions += 1  # Update collision score
                            # Create snowpile
                            if self.stats.amount_removed > 0:
                                self.stats.total_removed += self.stats.amount_removed
                                self.snowpile.add_coor(self.snowplow.grid_x, self.snowplow.grid_y)
                                self.stats.amount_removed = 0
                            self.draw_background()
                            self.snowplow.draw()
                            self.snowplow.get_available_directions(self.snowplow.grid_x, self.snowplow.grid_y)
                        self.stats.snowpiles = len(self.snowpile.coors)  # Update snowpile score
                        # Update display
                        self.draw_background()
                        self.snowplow.draw()
                        self.snowflake.draw()
                        self.snowpile.draw()
                        self.stats.display_info(self.font)

                # Set screen -----------------------------------------------------------------------------------------
                self.snowflake.draw()
                self.snowpile.draw()
                self.draw_grid()
                pygame.display.update()