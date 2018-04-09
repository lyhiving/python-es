import cv2 as cv
import numpy as np

cap = cv.VideoCapture('./res/video.mp4')

'''
read 读取视频
'''
# while(True):
#
#     ret, frame = cap.read()
#
#     gray = cv.cvtColor(frame, cv.COLOR_RGB2XYZ)
#
#     cv.imshow('frame', gray)
#
#     if cv.waitKey(1) == ord('q'):
#         break
#
# cap.release()
#
# cv.destroyAllWindows()

'''
save 保存视频
'''
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('./res/writeVideo.mp4', fourcc, 2.0, (740, 780), True)

while cap.isOpened():

    ret, frame = cap.read()

    if ret:

        # frame = cv.flip(frame, 1)

        frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

        out.write(frame)

        cv.imshow('frame', frame)

        if cv.waitKey(1) == 27:
            break
    else:
        break

cap.release()

out.release()

cv.destroyAllWindows()
