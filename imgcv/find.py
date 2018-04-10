import cv2 as cv
import numpy as np
import find_utils as utils


'''
读取图片
'''
img = cv.imread('./res/use3.jpg')
b, g, r = cv.split(img)
rgb_img = cv.merge([r, g, b])
hsv = cv.cvtColor(rgb_img, cv.COLOR_RGB2HSV)
'''
设置色彩空间阈值（将RGB转换为HSV颜色空间值），并且结果只能为一维数组
'''
lower_blue = utils.rgb2hsv([4, 155, 115])
upper_blue = utils.rgb2hsv([4, 165, 120])
'''
找到曝光点
'''
mask = cv.inRange(hsv, lower_blue, upper_blue)
res = cv.bitwise_and(rgb_img, rgb_img, mask=mask)
'''
找到所有的轮廓点
'''
gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)
img_res, contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
'''
绘制所有的轮廓，在原图上进行标记
'''
images = img
images = cv.drawContours(images, contours, -1, (0, 0, 0), 1)
find_array = []
'''
遍历所有的轮廓，找到梯度最大值的顶层与最小值的底层X/Y轴坐标点
'''
values = []
for index, i in enumerate(contours):
    if type(i) == np.ndarray and len(i) > 0:
        for j in i:
            utils.foreach_all_ndarray(j, values)
for i in values:
    print(i)
'''
展示所有的未/已处理的图片，进行对比
'''
# cv.imshow('frame', rgb_img)
# cv.imshow('mask', images)
# cv.imshow('res', res)
# k = cv.waitKey(0)
# if k == 27:
#     cv.destroyAllWindows()
