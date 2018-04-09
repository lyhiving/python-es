import cv2 as cv
import numpy as np

def draw_circe(e, x,y,flags,param):
    if e == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(img, (x, y), 100, (255, 0, 0), -1)

img = np.zeros((500, 500, 3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image', draw_circe)

while (1):
    cv.imshow('image', img)
    if cv.waitKey(1)&0xFF == ord('q'):#按q键退出
        break
cv.destroyAllWindows()