import cv2 as cv
import numpy as np


# RGB颜色值转HSV颜色空间值
def rgb2hsv(rgb):
    return np.array(cv.cvtColor(np.uint8([[rgb]]), cv.COLOR_RGB2HSV)[0][0])


# 遍历所有的N维轮廓数组，并传递最里层X,Y轴至指定数组中
def foreach_all_ndarray(arr, val_list=None):
    if type(arr) == np.ndarray:
        for item in arr:
            if type(item) == np.ndarray:
                foreach_all_ndarray(item, val_list)
            else:
                val_list.append([arr[0], arr[1]])
                break


def ndarray_split_group(values, items):
    for index, item in enumerate(values):
        if index == 0:
            items.append([item])
        else:
            if (values[0][1] + 100) > item[1] > (values[0][1] - 100):
                items[0].append(item)
            else:
                try:
                    items[1].append(item)
                except IndexError as e:
                    items.append([item])