import HARD_CODED_VALUES as HCV


class Stats:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.total_removed = 0
        self.amount_of_snow_moved = 0
        self.distance_travelled = 0
        self.collisions = 0
        self.snowpiles = 0

    def display_info(self, font):
        carry = font.render("Amount of Snow Moved: " + str(self.amount_of_snow_moved), True, HCV.WHITE)
        score = font.render("Score: " + str(self.total_removed), True, HCV.WHITE)
        distance = font.render("Distance Travelled: " + str(self.distance_travelled), True, HCV.WHITE)
        collision = font.render("Collisions: " + str(self.collisions), True, HCV.WHITE)
        snowpile = font.render("Snowpiles: " + str(self.snowpiles), True, HCV.WHITE)
        self.parent_screen.blit(carry, (HCV.CARRY_X, HCV.CARRY_Y))
        self.parent_screen.blit(score, (HCV.SCORE_X, HCV.SCORE_Y))
        self.parent_screen.blit(distance, (HCV.DISTANCE_X, HCV.DISTANCE_Y))
        self.parent_screen.blit(collision, (HCV.COLLISION_X, HCV.COLLISION_Y))
        self.parent_screen.blit(snowpile, (HCV.SNOWPILE_X, HCV.SNOWPILE_Y))