import cv2 as cv
import numpy as np

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


img = cv.imread('./res/use3.jpg')
b, g, r = cv.split(img)
rgb_img = cv.merge([r, g, b])
hsv = cv.cvtColor(rgb_img, cv.COLOR_RGB2HSV)
# print(cv.cvtColor(np.uint8([[[0, 255, 0]]]), cv.COLOR_RGB2HSV)[0][0])
lower_blue = np.array(cv.cvtColor(np.uint8([[[4, 155, 115]]]), cv.COLOR_RGB2HSV)[0][0])
upper_blue = np.array(cv.cvtColor(np.uint8([[[4, 165, 120]]]), cv.COLOR_RGB2HSV)[0][0])
# lower_blue = np.array([35, 43, 46])
# upper_blue = np.array([77, 255, 255])
mask = cv.inRange(hsv, lower_blue, upper_blue)
res = cv.bitwise_and(rgb_img, rgb_img, mask=mask)
# GRAY
gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)
img_res, contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# print(contours)
print(len(contours))
images = img
images = cv.drawContours(images, contours, 3, (0, 0, 0), 1)
# for i in contours:
#     print(i)
# cv.imshow('frame', rgb_img)
# cv.imshow('mask', images)
# cv.imshow('res', res)
# k = cv.waitKey(0)
# if k == 27:
#     cv.destroyAllWindows()

