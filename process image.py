import cv2 as cv
import numpy as np
import pandas as pd

parkingLot = cv.imread('Labelled Parking Lot.jpg')
parkingLot_hsv = cv.cvtColor(parkingLot, cv.COLOR_RGB2HSV)

# Define color ranges for masks
lower_green = np.array([50, 100, 100])
upper_green = np.array([70, 255, 255])
lower_blue = np.array([0, 100, 100])
upper_blue = np.array([10, 255, 255])
lower_red = np.array([110, 100, 100])
upper_red = np.array([130, 255, 255])

# create masks for boundary, parking spots, and entry
boundary_mask = cv.inRange(parkingLot_hsv, lower_blue, upper_blue)
parkingSpot_mask = cv.inRange(parkingLot_hsv, lower_red, upper_red)
entry_mask = cv.inRange(parkingLot_hsv, lower_green, upper_green)

# Use mask to extract the area of interest
boundary_result = cv.bitwise_and(parkingLot, parkingLot, mask=boundary_mask)
parkingSpot_result = cv.bitwise_and(parkingLot, parkingLot, mask=parkingSpot_mask)
entry_result = cv.bitwise_and(parkingLot, parkingLot, mask=entry_mask)

# Combine results for boundary, parking spots and entry
blend1 = cv.addWeighted(boundary_result, 1, parkingSpot_result, 1, 0)
blend2 = cv.addWeighted(blend1, 1, entry_result, 1, 0)

# Get X and Y coordinates of lines
x_boundary, y_boundary = np.where(np.all(boundary_result != [0, 0, 0], axis=2))
x_parkingSpot, y_parkingSpot = np.where(np.all(parkingSpot_result != [0, 0, 0], axis=2))
x_entry, y_entry = np.where(np.all(entry_result != [0, 0, 0], axis=2))
boundary_coordinates = np.column_stack((x_boundary, y_boundary))
parkingSpot_coordinates = np.column_stack((x_parkingSpot, y_parkingSpot))
entry_coordinates = np.column_stack((x_entry, y_entry))
df_boundary = pd.DataFrame(boundary_coordinates)
df_parkingSpot = pd.DataFrame(parkingSpot_coordinates)
df_entry = pd.DataFrame(entry_coordinates)
df_boundary.to_csv('boundary_coordinates.csv', index=False)
df_parkingSpot.to_csv('parkingSpot_coordinates.csv', index=False)
df_entry.to_csv('entry_coordinates.csv', index=False)

# Save final edited image
cv.imwrite('Edited Parking Lot.jpg', blend2)

# cv.imshow('Parking Lot', blend2)
# cv.waitKey(0)
# cv.destroyAllWindows()
