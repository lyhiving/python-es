import cv2 as cv
import numpy as np
import core.find_utils as utils
import math
from PIL import Image
import uuid


def run(path, is_rotate=False, point_num=9):
    print("检测图片的指标项目个数为：%s" % point_num)
    """
    读取图片
    """
    img = cv.imread(path)
    b, g, r = cv.split(img)
    rgb_img = cv.merge([r, g, b])
    shape = img.shape
    hsv = cv.cvtColor(rgb_img, cv.COLOR_RGB2HSV)
    '''
    设置色彩空间阈值（将RGB转换为HSV颜色空间值），并且结果只能为一维数组
    '''
    lower_hsv = utils.rgb2hsv([0, 0, 0])
    upper_hsv = utils.rgb2hsv([36, 36, 36])
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
    images = cv.drawContours(images, contours, -1, (0, 255, 0), 1)
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
    区分上下标示模块
    '''
    point_xy_one = sorted(items[0])
    point_xy_two = sorted(items[1])
    if point_xy_one[0][1] < point_xy_two[0][1]:
        point_xy_top = point_xy_one
        point_xy_bottom = point_xy_two
    else:
        point_xy_top = point_xy_two
        point_xy_bottom = point_xy_one
    point_xy_bottom_x_min = sorted(point_xy_bottom, key=lambda x: x[0])[0]
    point_xy_top_x_min = sorted(point_xy_top, key=lambda x: x[0])[0]
    '''
    判断图像特征值点数是否符合
    '''
    if len(items) != 2:
        return {
            'code': 403,
            'msg': '图像特征值未提取完整，请重新上传图片'
        }
    deviation = 20
    if point_xy_top_x_min[0] + deviation < point_xy_bottom_x_min[0] \
            or point_xy_bottom_x_min[0] < point_xy_top_x_min[0] - deviation:
        # 图像点位不正确，进行图片旋转纠正
        if not is_rotate:
            rad = math.atan2(point_xy_bottom_x_min[0]-point_xy_top_x_min[0],
                             point_xy_bottom_x_min[1]-point_xy_top_x_min[1]) * 180 / math.pi
            if rad < -1 or rad > 1:
                pilim = Image.open(path)
                im2 = pilim.convert('RGBA')
                rot = im2.rotate(-rad, expand=1)
                fff = Image.new('RGBA', rot.size, (255,)*4)
                out = Image.composite(rot, fff, rot)
                file_types = path.split(".")
                file_type = file_types[len(file_types)-1]
                new_path = './static/'+str(uuid.uuid1())+'.'+file_type
                out.convert(pilim.mode).save(new_path)
                return run(new_path, True)
        else:
            return {
                'code': 403,
                'msg': '图像点位不正确，请注意拍照姿势'
            }
    '''
    找寻下方模块的最顶点与上方模块最低点Y轴坐标
    '''
    point_xy_bottom_up = sorted(point_xy_bottom, key=lambda x: x[1])[0]
    point_xy_top_down = sorted(point_xy_top, key=lambda x: x[1], reverse=True)[0]
    '''
    进行检测项目个数 bottom_y - top_y / n
    '''
    cv.circle(images, (point_xy_bottom_up[0], point_xy_bottom_up[1]), 3, (0, 255, 0), 2)
    cv.circle(images, (point_xy_top_down[0], point_xy_top_down[1]), 3, (0, 255, 0), 2)
    y_value = (point_xy_bottom_up[1]-point_xy_top_down[1]) / (point_num * 2)
    x_width = (point_xy_one[len(point_xy_one)-1][0] - point_xy_one[0][0]) / 2
    '''
    计算出每个点位，并描绘至原图层
    '''
    colors = []
    last_y = point_xy_top_down[1]
    last_x = math.ceil(point_xy_one[0][0] + x_width)
    for i in range(0, point_num):
        if i == 0:
            last_y = last_y + y_value * 1.2
        else:
            last_y = last_y + y_value * 1.96
        last_y = math.ceil(last_y)
        point = (last_x, last_y)
        cv.circle(images, point, 3, (0, 255, 0), 2)
        # 获取rgb颜色值
        if last_y <= shape[0]:
            colors.append(utils.get_color_rgb(rgb_img[last_y, last_x]))
        # print(y_value, last_y, last_x)
    # cv.imwrite('../static/images.jpg', images)
    return {
        'code': 200,
        'msg': 'success',
        'data': colors
    }


if __name__ == "__main__":
    print(run('../static/use3.png'))
