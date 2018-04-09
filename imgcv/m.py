import cv2 as cv
import numpy as np


def get_color_rgb(px):
    s = ''

    for i in px:
        # print(i)
        s = s+str(i)+','

    print(s[0:-1])


# green = np.uint8([[[0, 255, 0]]])
# hsv_green = cv.cvtColor(green, cv.COLOR_BGR2HSV)  # 获取制定RGB颜色值的HSV颜色空间
# print(hsv_green)
img = cv.imread('./res/use2.jpg')
b, g, r = cv.split(img)
rgb_img = cv.merge([r, g, b])
# print(img.shape)
# print(img.size)
# print(img.dtype)
# cv.imshow('img', img)
# cv.waitKey(0)
# cv.destroyAllWindows()
get_color_rgb(rgb_img[1418, 1367])
get_color_rgb(rgb_img[1954, 1367])
get_color_rgb(rgb_img[2774, 1367])
# print(img.item(10,10,2))
# img.itemset((10,10,2),100)
# print(img.item(10,10,2))

