import cv2


img = cv2.imread("C:/Users/Administrator/Desktop/use.jpg", 1)

'''
显示图片
'''
cv2.imshow('image', img)

key = cv2.waitKey(0)

if key == 27:
    cv2.destroyAllWindows()
elif key == ord('s'):
    cv2.imwrite('C:/Users/Administrator/Desktop/testImg.png', img)
    print(2)

