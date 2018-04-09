import numpy as np
import cv2 as cv

img = np.zeros((512, 512, 3), np.uint8)

cv.line(img, (10, 10), (150, 450), (0, 255, 127), 2, cv.LINE_AA)

cv.namedWindow('img', cv.WINDOW_NORMAL)

cv.resizeWindow('img', 1000, 1000)

cv.imshow('img', img)

cv.waitKey(0)

cv.destroyAllWindows()
