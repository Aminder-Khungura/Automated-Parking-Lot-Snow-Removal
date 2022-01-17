import pygame
import HARD_CODED_VALUES as HCV
import Stats
import Barriers


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow (1).png')
        self.snowplow_character = pygame.transform.scale(self.snowplow_character, (HCV.SP_X_TRANSFORM, HCV.SP_Y_TRANSFORM))
        self.barriers = Barriers.Barriers(self.parent_screen)
        self.collision = False
        self.x_start = 0
        self.y_start = 0
        self.x_coor = 0
        self.y_coor = 0
        self.grid_x_start = 0
        self.grid_y_start = 0
        self.grid_x_coor = 0
        self.grid_y_coor = 0
        self.stats = Stats.Stats(self.parent_screen)
        self.start_pos_set = False
        self.available_directions = ["DOWN", "UP", "LEFT", "RIGHT"]
        self.last_move = "NONE"

    # Store the pixel and grid coordinates of the snowplow starting location
    def get_start_pos(self):
        self.x_coor, self.y_coor = pygame.mouse.get_pos()
        self.x_coor -= HCV.SNOWPLOW_IMG_OFFSET
        self.y_coor -= HCV.SNOWPLOW_IMG_OFFSET
        self.x_start = self.x_coor
        self.y_start = self.y_coor
        self.grid_x_start = (self.x_start + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        self.grid_y_start = (self.y_start + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
        self.grid_x_coor = (self.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        self.grid_y_coor = (self.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
        self.start_pos_set = True
        self.available_directions_for_next_move(self.grid_x_start, self.grid_y_start)
        print(self.available_directions)

    def draw_snowplow(self, x, y):
        self.parent_screen.blit(self.snowplow_character, [x, y])

    def detect_collision(self, x, y):
        coor = str(x) + ' ' + str(y)
        if coor in self.barriers.grid_boundary_coors or coor in self.barriers.grid_entry_coors:
            self.collision = True
        else:
            self.collision = False
        return self.collision

    def move_snowplow(self, event):
        original_x_coor = self.x_coor
        original_y_coor = self.y_coor
        if event.key == pygame.K_DOWN and "DOWN" in self.available_directions:
            self.y_coor += HCV.MOVE_Y
            self.grid_y_coor = (self.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "DOWN"
        if event.key == pygame.K_UP and "UP" in self.available_directions:
            self.y_coor -= HCV.MOVE_Y
            self.grid_y_coor = (self.y_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "UP"
        if event.key == pygame.K_LEFT and "LEFT" in self.available_directions:
            self.x_coor -= HCV.MOVE_X
            self.grid_x_coor = (self.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "LEFT"
        if event.key == pygame.K_RIGHT and "RIGHT" in self.available_directions:
            self.x_coor += HCV.MOVE_X
            self.grid_x_coor = (self.x_coor + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "RIGHT"
        return self.x_coor, self.y_coor, self.grid_x_coor, self.grid_y_coor, original_x_coor, original_y_coor

    def available_directions_for_next_move(self, grid_x, grid_y):
        # Remove the last movement direction from list of available moves, so snowplow doesnt continue into barrier
        if self.last_move in self.available_directions:
            self.available_directions.remove(self.last_move)

        # Check which directions you can move without having another collision, remove the directions that will result in collision from available moves
        for i in self.available_directions:
            if i == "DOWN":
                x = grid_x
                y = grid_y + 1
                collision_detected = self.detect_collision(x, y)
                if collision_detected:
                    self.available_directions.remove("DOWN")
            if i == "UP":
                x = grid_x
                y = grid_y - 1
                collision_detected = self.detect_collision(x, y)
                if collision_detected:
                    self.available_directions.remove("UP")
            if i == "LEFT":
                x = grid_x - 1
                y = grid_y
                collision_detected = self.detect_collision(x, y)
                if collision_detected:
                    self.available_directions.remove("LEFT")
            if i == "Right":
                x = grid_x + 1
                y = grid_y
                collision_detected = self.detect_collision(x, y)
                if collision_detected:
                    self.available_directions.remove("Right")

