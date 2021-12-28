import cv2 as cv
import numpy as np

parkingLot = cv.imread('Labelled Parking Lot.jpg')
parkingLot_hsv = cv.cvtColor(parkingLot, cv.COLOR_RGB2HSV)

lower_green = np.array([50, 100, 100])
upper_green = np.array([70, 255, 255])
lower_blue = np.array([0, 100, 100])
upper_blue = np.array([10, 255, 255])
lower_red = np.array([110, 100, 100])
upper_red = np.array([130, 255, 255])

boundary_mask = cv.inRange(parkingLot_hsv, lower_blue, upper_blue)
parkingSpot_mask = cv.inRange(parkingLot_hsv, lower_red, upper_red)
entry_mask = cv.inRange(parkingLot_hsv, lower_green, upper_green)

boundary_result = cv.bitwise_and(parkingLot, parkingLot, mask=boundary_mask)
parkingSpot_result = cv.bitwise_and(parkingLot, parkingLot, mask=parkingSpot_mask)
entry_result = cv.bitwise_and(parkingLot, parkingLot, mask=entry_mask)

blend1 = cv.addWeighted(boundary_result, 1, parkingSpot_result, 1, 0)
blend2 = cv.addWeighted(blend1, 1, entry_result, 1, 0)
cv.imshow('Parking Lot', blend2)

cv.waitKey(0)
cv.destroyAllWindows()