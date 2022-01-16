import HARD_CODED_VALUES as HCV


class Stats:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.points = 0
        self.amount_of_snow_held = 0
        self.distance_travelled = 0
        self.collisions = 0

    def display_info(self, font):
        carry = font.render("Amount of Snow Currently Held: " + str(self.amount_of_snow_held), True, HCV.WHITE)
        score = font.render("Score: " + str(self.points), True, HCV.WHITE)
        distance = font.render("Distance Travelled : " + str(self.distance_travelled), True, HCV.WHITE)
        collision = font.render("Collisions : " + str(self.collisions), True, HCV.WHITE)
        self.parent_screen.blit(carry, (HCV.CARRY_X, HCV.CARRY_Y))
        self.parent_screen.blit(score, (HCV.SCORE_X, HCV.SCORE_Y))
        self.parent_screen.blit(distance, (HCV.DISTANCE_X, HCV.DISTANCE_Y))
        self.parent_screen.blit(collision, (HCV.COLLISION_X, HCV.COLLISION_Y))