from queue import PriorityQueue

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