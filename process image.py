import cv2 as cv
import numpy as np

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
boundary_result = cv.bitwise_and(parkingLot_hsv, parkingLot_hsv, mask=boundary_mask)
parkingSpot_result = cv.bitwise_and(parkingLot_hsv, parkingLot_hsv, mask=parkingSpot_mask)
entry_result = cv.bitwise_and(parkingLot_hsv, parkingLot_hsv, mask=entry_mask)

# Combine results for boundary, parking spots and entry
blend1 = cv.addWeighted(boundary_result, 1, parkingSpot_result, 1, 0)
blend2 = cv.addWeighted(blend1, 1, entry_result, 1, 0)

# Clean up final image before saving
# kernel_erode = np.ones((2, 2), np.uint8)
# kernel_close = np.ones((15, 15), np.uint8)
# erode = cv.erode(blend2, kernel_erode)
# closing = cv.morphologyEx(erode, cv.MORPH_CLOSE, kernel_close)

# Save final edited image
pic_RGB = cv.cvtColor(blend2, cv.COLOR_HSV2RGB)
cv.imwrite('Edited Parking Lot.jpg', pic_RGB)

# cv.imshow('Parking Lot', closing)
# cv.waitKey(0)
# cv.destroyAllWindows()
