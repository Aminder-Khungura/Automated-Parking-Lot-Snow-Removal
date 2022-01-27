import pygame
import HARD_CODED_VALUES as HCV
import Barriers
import Snowflake
from ASTAR import pathfinding
from scipy import spatial


class Snowplow:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snowplow_character = pygame.image.load('snowplow.png')
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
        self.available_directions = ["DOWN", "UP", "LEFT", "RIGHT", "DOWN/LEFT", "DOWN/RIGHT", "UP/LEFT", "UP/RIGHT"]
        self.last_move = 'NONE'
        self.snowflake_coors = [[]]
        self.snowflake = Snowflake.Snowflake(self.parent_screen)

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

    def draw(self):
        self.parent_screen.blit(self.snowplow_character, [self.x, self.y])

    def detect_collision(self, grid_x, grid_y):
        coor = str(grid_x) + ' ' + str(grid_y)
        if coor in self.barriers.grid_boundary_coors or coor in self.barriers.grid_entry_coors:
            self.collision = True
        else:
            self.collision = False
        return self.collision

    def get_available_directions(self, grid_x, grid_y):
        self.available_directions = ["DOWN", "UP", "LEFT", "RIGHT", "DOWN/LEFT", "DOWN/RIGHT", "UP/LEFT", "UP/RIGHT"]
        # Remove the last movement direction from list of available moves, so snowplow doesnt continue into barrier
        if self.last_move in self.available_directions and self.collision:
            self.available_directions.remove(self.last_move)
        # Check which directions you can move without having another collision, remove the directions that will result in collision from available moves
        for i in self.available_directions:
            if "DOWN" == i:
                x = grid_x
                y = grid_y + 1
            elif "UP" == i:
                x = grid_x
                y = grid_y - 1
            elif "LEFT" == i:
                x = grid_x - 1
                y = grid_y
            elif "RIGHT" == i:
                x = grid_x + 1
                y = grid_y
            elif "DOWN/LEFT" == i:
                x = grid_x - 1
                y = grid_y + 1
            elif "DOWN/RIGHT" == i:
                x = grid_x + 1
                y = grid_y + 1
            elif "UP/LEFT" == i:
                x = grid_x - 1
                y = grid_y - 1
            elif "UP/RIGHT" == i:
                x = grid_x + 1
                y = grid_y - 1
            else:
                print('ERROR --- NO AVAILABLE DIRECTIONS TO MOVE')
                x, y = 0, 0
            collision_detected = self.detect_collision(x, y)
            if collision_detected:
                self.available_directions.remove(i)

    def loop_till_collision(self, inc_x, inc_y):
        snow = self.snowflake_coors[:]
        x, y = self.grid_x,  self.grid_y
        coor = [x, y]
        snow_collected = 0
        snow_collection_point_multiplier = 2
        distance_travelled = 0
        collision = False
        loop_counter = 0
        while not collision:
            if coor in snow:
                snow_collected += 1 * snow_collection_point_multiplier
                snow.remove(coor)
            x += inc_x
            y += inc_y
            distance_travelled += 1
            coor = [x, y]
            collision = self.detect_collision(x, y)
            # To Fix the bug caused by an available direction/position outside the boundary, resulting in loop searching forever in that direction. Outside boundary therefore will never have collision.
            loop_counter += 1
            if loop_counter > 50:
                score, snow_collected, distance_travelled, end_coor = -9999, -9999, 9999, [0, 0]
                return score, snow_collected, distance_travelled, coor
        if coor in snow:
            snow_collected += 1 * snow_collection_point_multiplier
            snow.remove(coor)
        score = snow_collected - distance_travelled
        return score, snow_collected, distance_travelled, coor

    def greedy_algorithm(self):
        scores = {}
        snow_collection = {}
        distances = {}
        end_coors = {}
        for i in self.available_directions:
            if "DOWN" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=0, inc_y=1)
            elif "UP" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=0, inc_y=-1)
            elif "LEFT" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=-1, inc_y=0)
            elif "RIGHT" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=1, inc_y=0)
            elif "DOWN/LEFT" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=-1, inc_y=1)
            elif "DOWN/RIGHT" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=1, inc_y=1)
            elif "UP/LEFT" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=-1, inc_y=-1)
            elif "UP/RIGHT" == i:
                score, snow_collected, distance_travelled, end_coor = self.loop_till_collision(inc_x=1, inc_y=-1)
            else:
                print('ERROR --- NO AVAILABLE DIRECTIONS TO MOVE')
                score, snow_collected, distance_travelled, end_coor = 0, 0, 0, [0, 0]
            scores[i] = score
            snow_collection[i] = snow_collected
            distances[i] = distance_travelled
            end_coors[i] = end_coor
        direction = max(scores, key=scores.get)
        # Check if snow collected
        if snow_collection[direction] > 0:
            snow_found = True
            num_of_moves = distances[direction]
        else:
            direction = 'NONE'
            num_of_moves = 1
            snow_found = False
        return direction, num_of_moves, snow_found

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
        elif next_direction == "RIGHT":
            self.x += HCV.MOVE_X
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "RIGHT"
        elif next_direction == "DOWN/LEFT":
            self.x -= HCV.MOVE_X
            self.y += HCV.MOVE_Y
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "DOWN/LEFT"
        elif next_direction == "DOWN/RIGHT":
            self.x += HCV.MOVE_X
            self.y += HCV.MOVE_Y
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "DOWN/RIGHT"
        elif next_direction == "UP/LEFT":
            self.x -= HCV.MOVE_X
            self.y -= HCV.MOVE_Y
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "UP/LEFT"
        elif next_direction == "UP/RIGHT":
            self.x += HCV.MOVE_X
            self.y -= HCV.MOVE_Y
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "UP/RIGHT"
        else:
            print('ERROR --- NO DIRECTIONS GIVEN')

    def get_closest_snow(self):
        tree = spatial.KDTree(self.snowflake_coors)
        distance_to_snow, index = tree.query([self.grid_x, self.grid_y])
        coor = self.snowflake_coors[index]
        closest_snow_flake = (coor[0], coor[1])
        return closest_snow_flake

    def reposition(self):
        start_coor = (self.grid_x, self.grid_y)
        end_coor = self.get_closest_snow()
        path = pathfinding(self.snowflake.maze, start_coor, end_coor)
        direction = 'NONE'
        for loc in path[1:]:
            new_x = loc[0]
            new_y = loc[1]
            if new_x < self.grid_x and new_y == self.grid_y:
                direction = 'LEFT'
            elif new_x > self.grid_x and new_y == self.grid_y:
                direction = 'RIGHT'
            elif new_y < self.grid_y and new_x == self.grid_x:
                direction = 'UP'
            elif new_y > self.grid_y and new_x == self.grid_x:
                direction = 'DOWN'
            elif new_x < self.grid_x and new_y > self.grid_y:
                direction = 'DOWN/LEFT'
            elif new_x > self.grid_x and new_y > self.grid_y:
                direction = 'DOWN/RIGHT'
            elif new_y < self.grid_y and new_x < self.grid_x:
                direction = 'UP/LEFT'
            elif new_y < self.grid_y and new_x > self.grid_x:
                direction = 'UP/RIGHT'
            else:
                print("ERROR --- CAN'T DETERMINE DIRECTION")
            self.greedy_movement(direction)
        num_of_moves = len(path[1:])
        return num_of_moves

    def dynamic_programming(self, coors):
        pass