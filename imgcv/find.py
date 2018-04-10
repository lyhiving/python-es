import cv2 as cv
import numpy as np
import find_utils as utils
import math

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
lower_hsv = utils.rgb2hsv([4, 155, 115])
upper_hsv = utils.rgb2hsv([4, 165, 120])
'''
找到曝光点
'''
mask = cv.inRange(hsv, lower_hsv, upper_hsv)
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
'''
进行轮廓点位分组
'''
items = []
utils.ndarray_split_group(values, items)
'''
判断图像特征值点数是否符合
'''
if len(items) != 2:
    print('图像特征值未提取完整，请重新上传图片')
    exit(0)
point_xy_one = sorted(items[0])
point_xy_two = sorted(items[1])
if point_xy_one[0][0] + 3 < point_xy_two[0][0] or point_xy_two[0][0] < point_xy_one[0][0] - 3:
    print('图像点位不正确，请注意拍照姿势')
    exit(0)
'''
区分上下标示模块
'''
point_xy_top = None
point_xy_bottom = None
if point_xy_one[0][1] < point_xy_two[0][1]:
    point_xy_top = point_xy_one
    point_xy_bottom = point_xy_two
else:
    point_xy_top = point_xy_two
    point_xy_bottom = point_xy_one
# TODO 找寻下方模块的最顶点与上方模块最低点Y轴坐标
point_xy_bottom_up = sorted(point_xy_bottom, key=lambda x: x[1])[0]
point_xy_top_down = sorted(point_xy_top, key=lambda x: x[1], reverse=True)[0]
# TODO 进行检测项目个数 bottom_y - top_y / n
print(point_xy_bottom_up)
print(point_xy_top_down)
cv.circle(images, (point_xy_bottom_up[0], point_xy_bottom_up[1]), 3, (0, 255, 0), 2)
cv.circle(images, (point_xy_top_down[0], point_xy_top_down[1]), 3, (0, 255, 0), 2)
y_value = (point_xy_bottom_up[1]-point_xy_top_down[1]) / 30
x_width = (point_xy_one[len(point_xy_one)-1][0] - point_xy_one[0][0]) / 2
# TODO 计算出每个点位，并描绘至原图层
points = []
last_y = point_xy_top_down[1]
last_x = math.ceil(point_xy_one[0][0] + x_width)
for i in range(0, 15):
    if i == 0:
        last_y = last_y + y_value * 1.2
    else:
        last_y = last_y + y_value * 1.96
    point = (last_x, math.ceil(last_y))
    cv.circle(images, point, 3, (0, 255, 0), 2)
    points.append(point)
'''
展示所有的未/已处理的图片，进行对比
'''
# cv.imshow('frame', rgb_img)
# cv.imshow('mask', mask)
# cv.imshow('res', res)
cv.imshow('result', images)
k = cv.waitKey(0)
if k == 27:
    cv.destroyAllWindows()
