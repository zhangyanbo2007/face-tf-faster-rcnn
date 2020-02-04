import cv2
import numpy as np
img=cv2.imread('test_image/test.jpg')
imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(imgray,127,255,0)
image,contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow('imageshow',image)  # 显示返回值image，其实与输入参数的thresh原图没啥区别
cv2.imwrite("test_image/imageshow.jpg", image)
cv2.waitKey()
print(np.size(contours))  #   得到该图中总的轮廓数量
print(contours[0])   #  打印出第一个轮廓的所有点的坐标， 更改此处的0，为0--（总轮廓数-1），可打印出相应轮廓所有点的坐标
print(hierarchy) #打印出相应轮廓之间的关系
img=cv2.drawContours(img,[contours[0]],-1,(0,255,0),10)  #标记处编号为0的轮廓，此处img为三通道才能显示轮廓
# cv2.imshow('drawimg',img)
cv2.imwrite("test_image/contors_0.jpg", img)
cv2.waitKey()
