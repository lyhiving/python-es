import cv2

from matplotlib import pyplot as plt

img = cv2.imread('./res/use2.jpg', -1)
b, g, r = cv2.split(img)
rgb_img = cv2.merge([r, g, b])
plt.imshow(rgb_img)
plt.xticks([]), plt.yticks([])
plt.show()
