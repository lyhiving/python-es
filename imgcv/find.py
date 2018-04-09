import cv2 as cv
import numpy as np

img = cv.imread('./res/use.jpg')
b, g, r = cv.split(img)
rgb_img = cv.merge([r, g, b])

hsv = cv.cvtColor(rgb_img, cv.COLOR_RGB2HSV)

lower_blue = np.array(cv.cvtColor(np.uint8([[[0, 0, 0]]]), cv.COLOR_BGR2HSV))
upper_blue = np.array(cv.cvtColor(np.uint8([[[5, 5, 5]]]), cv.COLOR_BGR2HSV))
mask = cv.inRange(hsv, lower_blue, upper_blue)
res = cv.bitwise_and(rgb_img, rgb_img, mask=mask)
# GRAY
# gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)
img_res, contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print(contours)
print(len(contours))
imag = img
for i in contours:
    imag = cv.drawContours(imag, i, 3, (0, 255, 0), 3)
# cv.imshow('frame', rgb_img)
cv.imshow('mask', imag)
# cv.imshow('res', res)
cv.waitKey(0)
cv.destroyAllWindows()
