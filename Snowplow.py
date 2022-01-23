import pygame
import HARD_CODED_VALUES as HCV
import Barriers
import ASTAR
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
        self.snowflake_coors = [[]]
        self.closest_snow_flake = []
        self.maze = [[0] * 50] * 50
        self.maze = self.make_maze()

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
        snow = self.snowflake_coors[:]
        x, y = self.grid_x,  self.grid_y
        coor = [x, y]
        snow_collected = 0
        snow_collection_point_multiplier = 12
        distance_travelled = 0
        collision = False
        while not collision:
            if coor in snow:
                snow_collected += 1 * snow_collection_point_multiplier
                snow.remove(coor)
            x += inc_x
            y += inc_y
            distance_travelled += 1
            coor = [x, y]
            collision = self.detect_collision(x, y)
        if coor in snow:
            snow_collected += 1 * snow_collection_point_multiplier
            snow.remove(coor)
        score_down = snow_collected - distance_travelled
        return score_down, snow_collected, distance_travelled, coor

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
        # Check if snow collected
        if snow_collection[direction] > 0:
            num_of_moves = distances[direction]
        else:
            print('There is No snow available at this position.')
            self.get_closest_snow()
            neighbours = self.get_neighbours()
            start_coor = [self.grid_x,  self.grid_y]
            print('Short:', self.astar(self.maze, neighbours, start_coor, self.closest_snow_flake))
        print('Move:', direction, num_of_moves, ' spaces.')
        print('Scores:', scores)
        print('-----------------------------------------------------------')
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
        elif next_direction == "RIGHT":
            self.x += HCV.MOVE_X
            self.grid_x = (self.x + HCV.SNOWPLOW_IMG_OFFSET) // HCV.BLOCK_WIDTH
            self.last_move = "RIGHT"
        else:
            print('ERROR --- NO DIRECTIONS GIVEN')

    def get_closest_snow(self):
        tree = spatial.KDTree(self.snowflake_coors)
        distance_to_snow, index = tree.query([self.grid_x, self.grid_y])
        print('Current position:', self.grid_x, self.grid_y)
        self.closest_snow_flake = self.snowflake_coors[index]
        print('Closest snow flake:', self.closest_snow_flake)

    def get_neighbours(self):
        x = self.grid_x
        y = self.grid_y
        neighbours = [[]]
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
                print('ERROR --- NO AVAILABLE DIRECTIONS TO CHECK')
                inc_x, inc_y = 0, 0
            neighbours.append([x + inc_x, y + inc_y])
        return neighbours

    def make_maze(self):
        for index, i in enumerate(self.maze):
            if i in self.barriers.grid_boundary_coors_INT:
                self.maze[index] = 1
            if i in self.barriers.grid_entry_coors_INT:
                self.maze[index] = 1
        return self.maze

    def dynamic_programming(self, coors):
        pass

    def astar(self, maze, neighbours, start, end):
        # Create start and end node
        start_node = ASTAR.Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = ASTAR.Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in neighbours:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = ASTAR.Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)