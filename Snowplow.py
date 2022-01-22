import pygame
import HARD_CODED_VALUES as HCV
import Barriers
from scipy import spatial


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
        self.last_move = 'NONE'
        self.snow_coors = []

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
            else:
                print('ERROR --- NO AVAILABLE DIRECTIONS TO MOVE')
                x, y = 0, 0
            collision_detected = self.detect_collision(x, y)
            if collision_detected:
                self.available_directions.remove(i)

    def loop_till_collision(self, inc_x, inc_y):
        x = self.grid_x
        y = self.grid_y
        coor = [x, y]
        snow_collected = 0
        snow_collection_point_multiplier = 12
        distance_travelled = 0
        collision = False
        # Loop until snowplow has a collision
        while not collision:
            if coor in self.snow_coors:
                snow_collected += 1 * snow_collection_point_multiplier
                self.snow_coors.remove(coor)
            x += inc_x
            y += inc_y
            distance_travelled += 1
            coor = [x, y]
            collision = self.detect_collision(x, y)
        # Check if there is snow in the snowplow's finish position
        if coor in self.snow_coors:
            snow_collected += 1 * snow_collection_point_multiplier
            self.snow_coors.remove(coor)
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
            else:
                print('ERROR --- NO AVAILABLE DIRECTIONS TO MOVE')
                score, snow_collected, distance_travelled, end_coor = 0, 0, 0, [0, 0]
            scores[i] = score
            snow_collection[i] = snow_collected
            distances[i] = distance_travelled
            end_coors[i] = end_coor

        direction = max(scores, key=scores.get)
        # Check if this move collects any snow, if it does not just move 1 cell in the direction selected above.
        # Done to prevent snowplow from getting stuck moving back and forth
        if snow_collection[direction] > 0:
            num_of_moves = distances[direction]
        else:
            print('There is No snow available at this position.')
            coors_to_check = self.get_coors_to_check()
            print('Re-evaluate @', coors_to_check)
            results = self.find_snow(coors_to_check)
            print('Results:', results)
            direction = min(results, key=results.get)
            num_of_moves = results[direction]
            if num_of_moves == 9999:
                num_of_moves = 1
        print('Move:', direction, num_of_moves, ' spaces.')
        print('Scores:', scores)
        tree = spatial.KDTree(self.snow_coors)
        distance_to_snow, index = tree.query([self.grid_x, self.grid_y])
        print('Current position:', self.grid_x, self.grid_y)
        print('Closest snow flake:', self.snow_coors[index])
        print('-----------------------------------------------------------')
        print('-----------------------------------------------------------')
        return direction, num_of_moves

    def greedy_movement(self, direction):
        if direction == "DOWN":
            self.y += HCV.MOVE_Y
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "DOWN"
        elif direction == "UP":
            self.y -= HCV.MOVE_Y
            self.grid_y = (self.y + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_HEIGHT
            self.last_move = "UP"
        elif direction == "LEFT":
            self.x -= HCV.MOVE_X
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "LEFT"
        elif direction == "RIGHT":
            self.x += HCV.MOVE_X
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "RIGHT"
        else:
            print('ERROR --- NO DIRECTION GIVEN')

    def get_coors_to_check(self):
        x = self.grid_x
        y = self.grid_y
        coors_to_check = {}
        for i in self.available_directions:
            if "DOWN" == i:
                inc_x = 0
                inc_y = 1
            elif "UP" == i:
                inc_x = 0
                inc_y = -1
            elif "LEFT" == i:
                inc_x = -1
                inc_y = 0
            elif "RIGHT" == i:
                inc_x = 1
                inc_y = 0
            else:
                print('ERROR --- NO AVAILABLE DIRECTIONS TO MOVE')
                inc_x, inc_y = 0, 0
            new_x = x + inc_x
            new_y = y + inc_y
            coors_to_check[i] = [new_x, new_y]
        return coors_to_check

    def find_snow(self, coors_to_check):
        results = {}
        for key in coors_to_check:
            coor = coors_to_check[key]
            x = coor[0]
            y = coor[1]
            self.last_move = 'NONE'  # Because there was no collision we set last move to 'None'
            self.get_available_directions(x, y)
            print('Check available directions @', coor)
            results[key] = 9999
            if "DOWN" in self.available_directions:
                distance_travelled = self.loop_till_snow(x, y, inc_x=0, inc_y=1, direction="DOWN")
                if distance_travelled < results[key]:
                    results[key] = distance_travelled
            if "UP" in self.available_directions:
                distance_travelled = self.loop_till_snow(x, y, inc_x=0, inc_y=-1, direction="UP")
                if distance_travelled < results[key]:
                    results[key] = distance_travelled
            if "LEFT" in self.available_directions:
                distance_travelled = self.loop_till_snow(x, y, inc_x=-1, inc_y=0, direction="LEFT")
                if distance_travelled < results[key]:
                    results[key] = distance_travelled
            if "RIGHT" in self.available_directions:
                distance_travelled = self.loop_till_snow(x, y, inc_x=1, inc_y=0, direction="RIGHT")
                if distance_travelled < results[key]:
                    results[key] = distance_travelled
            return results

    def loop_till_snow(self, x, y, inc_x, inc_y, direction):
        coor = [x, y]
        looking_for_snow = True
        snow_found = False
        distance_travelled = 0
        while looking_for_snow:
            if coor in self.snow_coors:
                snow_found = True
                looking_for_snow = False
            else:
                x += inc_x
                y += inc_y
                distance_travelled += 1
                coor = [x, y]
                collision = self.detect_collision(x, y)
                if collision:
                    looking_for_snow = False
        if snow_found:
            print('FOUND SNOW', '@', direction, coor)
        else:
            distance_travelled = 9999
            print('FAILED', '@', direction, coor)
        return distance_travelled

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
