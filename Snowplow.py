import pygame
import HARD_CODED_VALUES as HCV
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
        self.x = 0
        self.y = 0
        self.grid_x_start = 0
        self.grid_y_start = 0
        self.grid_x = 0
        self.grid_y = 0
        self.start_pos_set = False
        self.available_directions = ["DOWN", "UP", "LEFT", "RIGHT"]
        self.last_move = "NONE"

    # Store the pixel and grid coordinates of the snowplow starting location
    def get_start_pos(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.x -= HCV.SNOWPLOW_IMG_OFFSET
        self.y -= HCV.SNOWPLOW_IMG_OFFSET
        self.x_start = self.x
        self.y_start = self.y
        self.grid_x_start = (self.x_start + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        self.grid_y_start = (self.y_start + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
        self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
        self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
        self.start_pos_set = True
        self.get_available_directions(self.grid_x_start, self.grid_y_start)

    def draw(self, x, y):
        self.parent_screen.blit(self.snowplow_character, [x, y])

    def detect_collision(self, grid_x, grid_y):
        coor = str(grid_x) + ' ' + str(grid_y)
        if coor in self.barriers.grid_boundary_coors or coor in self.barriers.grid_entry_coors:
            self.collision = True
        else:
            self.collision = False
        return self.collision

    def get_available_directions(self, grid_x, grid_y):
        self.available_directions = ["DOWN", "UP", "LEFT", "RIGHT"]
        # Remove the last movement direction from list of available moves, so snowplow doesnt continue into barrier
        if self.last_move in self.available_directions:
            self.available_directions.remove(self.last_move)
        # Check which directions you can move without having another collision, remove the directions that will result in collision from available moves
        if "DOWN" in self.available_directions:
            x = grid_x
            y = grid_y + 1
            collision_detected = self.detect_collision(x, y)
            if collision_detected:
                self.available_directions.remove("DOWN")
        if "UP" in self.available_directions:
            x = grid_x
            y = grid_y - 1
            collision_detected = self.detect_collision(x, y)
            if collision_detected:
                self.available_directions.remove("UP")
        if "LEFT" in self.available_directions:
            x = grid_x - 1
            y = grid_y
            collision_detected = self.detect_collision(x, y)
            if collision_detected:
                self.available_directions.remove("LEFT")
        if "RIGHT" in self.available_directions:
            x = grid_x + 1
            y = grid_y
            collision_detected = self.detect_collision(x, y)
            if collision_detected:
                self.available_directions.remove("RIGHT")

    def loop_till_collision(self, inc_x, inc_y, coors):
        snow_coors = coors[:]  # Copy list this way so changes made to copy don't affect original
        x = self.grid_x
        y = self.grid_y
        coor = [x, y]
        snow_collected = 0
        snow_collection_point_multiplier = 2
        distance_travelled = 0
        collision = False
        while not collision:
            if coor in snow_coors:
                snow_collected += 1 * snow_collection_point_multiplier
                snow_coors.remove(coor)

            x += inc_x
            y += inc_y
            distance_travelled += 1
            coor = [x, y]
            collision = self.detect_collision(x, y)

        if coor in snow_coors:
            snow_collected += 1 * snow_collection_point_multiplier
            snow_coors.remove(coor)

        score_down = snow_collected - distance_travelled
        return score_down, snow_collected, distance_travelled, coor

    def greedy_algorithm(self, coors):
        snowflake_coors = coors[:]
        scores = {"DOWN": -9999, "UP": -9999, "LEFT": -9999, "RIGHT": -9999}
        snow_collection = {"DOWN": -9999, "UP": -9999, "LEFT": -9999, "RIGHT": -9999}
        distances = {"DOWN": 9999, "UP": 9999, "LEFT": 9999, "RIGHT": 9999}
        end_coors = {"DOWN": [0, 0], "UP": [0, 0], "LEFT": [0, 0], "RIGHT": [0, 0]}
        if "DOWN" in self.available_directions:
            score_down, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=0, inc_y=1, coors=snowflake_coors)
            scores['DOWN'] = score_down
            snow_collection['DOWN'] = snow_collected
            distances['DOWN'] = distance_travelled
            end_coors['DOWN'] = end_coor
        if "UP" in self.available_directions:
            score_up, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=0, inc_y=-1, coors=snowflake_coors)
            scores['UP'] = score_up
            snow_collection['UP'] = snow_collected
            distances['UP'] = distance_travelled
            end_coors['UP'] = end_coor
        if "LEFT" in self.available_directions:
            score_left, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=-1, inc_y=0, coors=snowflake_coors)
            scores['LEFT'] = score_left
            snow_collection['LEFT'] = snow_collected
            distances['LEFT'] = distance_travelled
            end_coors['LEFT'] = end_coor
        if "RIGHT" in self.available_directions:
            score_right, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=1, inc_y=0, coors=snowflake_coors)
            scores['RIGHT'] = score_right
            snow_collection['RIGHT'] = snow_collected
            distances['RIGHT'] = distance_travelled
            end_coors['RIGHT'] = end_coor

        direction = max(scores, key=scores.get)
        num_of_moves = distances[direction]
        print('------------------------------------------------')
        print('Scores:', scores)
        print('Snow collected:', snow_collection)
        print('Distances:', distances)
        print('End Pos:', end_coors)
        print('Move:', direction, ' ', 'Spaces:', num_of_moves)
        print('Available Directions:', self.available_directions)
        print('------------------------------------------------')
        print('\n')
        return direction, num_of_moves

    def greedy_movement(self, next_direction):
        if next_direction == "DOWN":
            self.y += HCV.MOVE_Y
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "DOWN"
        elif next_direction == "UP":
            self.y -= HCV.MOVE_Y
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "UP"
        elif next_direction == "LEFT":
            self.x -= HCV.MOVE_X
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "LEFT"
        else:  # next_direction == "RIGHT"
            self.x += HCV.MOVE_X
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "RIGHT"

    def dynamic_programming(self, coors):
        pass

# Ideally every move should remove a snowflake
# Remove all snowflakes
# End with snowplow at entry
# Snowplow can not turn until it deposits the snow it is currently holding, deposits must be at cell adjacent to boundary

# 1) Check paths available from current position (up, down, left, right):
#       a) count collectable snowflakes on that path until collision with boundary/entry
#       b) count cells travelled on that path until collision with boundary/entry
# 2) At boundary/entry location check paths available
#       a) Ensure that snowflakes removed from previous move are not recounted
#       b)

# Calculate GRADE for paths (i.e. from boundary cell to perpendicular boundary cell), these two cells will have the same score therefore can save scores to speed up process
# GRADE = Score - Distance Travelled
