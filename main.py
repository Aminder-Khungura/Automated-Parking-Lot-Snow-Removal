import cv2
import numpy as np

parkingLot = cv2.imread('Labelled Parking Lot.jpg')
parkingLot_hsv = cv2.cvtColor(parkingLot, cv2.COLOR_BGR2RGB)

boundary = np.array([63, 72, 204])
parkingSpot = np.array([237, 28, 36])
entry_exit = np.array([34, 177, 76])

cv2.imshow('Parking Lot', parkingLot)
cv2.waitKey(0)
cv2.destroyAllWindows()