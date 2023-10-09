# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:19:34 2023

@author: jeeki
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 09:37:24 2023

@author: jeeki
"""

import imutils
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from imutils.perspective import four_point_transform
import cv2
import numpy as np
from scipy import ndimage
import pandas as pd
import matplotlib.pyplot as plt
import os
os.chdir('C:/Users/jeeki/Desktop/flower_size')


# define a resizing function
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def show(image,x=30,y=7):
  img=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  plt.figure(figsize=(x,y))
  plt.imshow(img)

image = cv2.imread("temp.jpg")
#image = cv2.GaussianBlur(image, (5,5), 0)

image = cv2.rotate(image, cv2.ROTATE_180)

#show(image)


arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)

detected=cv2.aruco.drawDetectedMarkers(image,markerCorners, markerIds)

#find aruco markers for cuttouts and for reference size
aruco_areas=[]
aruco_lenth=[]
aruco_width=[]
for area in markerCorners: 
    aruco_areas.append(cv2.contourArea(area))
    rect = cv2.minAreaRect(area)
    aruco_lenth.append(rect[1][1])
    aruco_width.append(rect[1][0])

    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(image,[box],0,(255,0,0),2)

#show(image)

#average length and widths of aruco markers 8 numbers
average_length=np.average(aruco_lenth+aruco_width)
average_length

#make aruco markers blue
for middle in markerCorners:
    M = cv2.moments(middle)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    (cX,cY) 
   # image = cv2.circle(image, (cX,cY), radius=int(average_length*1.1), color=(0, 0, 255), thickness=-1)
    image = cv2.circle(image, (cX,cY), radius=int(average_length*1.3), color=(255, 0, 0), thickness=-1)

#show(image)


#cropped = image


#show(image)


hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)




# define range of blue color in HSV
#
# Use this to isolate the blue background
#
lower_blue = np.array([90,0,0])
upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask_blue = cv2.bitwise_not(mask_blue)
#show(mask_blue)



#use contour detection to measure plant size
# find contours in the thresholded image
cnts = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

cnts_list = list(cnts)

# isolate the small ones and remove

dust_thresh = 2000

new_cnts_list=[]
for i in cnts_list:
    if cv2.contourArea(i) > dust_thresh:
        new_cnts_list.append(i)



area=[]
rejected=[]
length=[]
width=[]

print("[INFO] {} items found please adjust dust threshold or binary threshold if wrong".format(len(new_cnts_list)))




for c in new_cnts_list:
    if cv2.contourArea(c) > dust_thresh:
        area.append(cv2.contourArea(c))
    # draw a circle enclosing the object
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(1), (0, 0, 255), 10)
    #cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
    #    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # find the length and width of object
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image,[box],0,(0,255,0),5)

    
    # save length and width of object
        length.append(rect[1][1])
        width.append(rect[1][0])

        w=round(rect[1][1] * 12.7  / average_length,2)
        h=round(rect[1][0] * 12.7 / average_length,2)
        cv2.putText(image, "w={}, h={}".format(w,h), (int(rect[0][0]),int(rect[0][1])),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
    if cv2.contourArea(c) < dust_thresh:
        rejected.append(cv2.contourArea(c))   

cv2.putText(image,"[INFO] {} items found".format(len(new_cnts_list)),(100,100),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)
#show(image)

cv2.imwrite("contours.jpg",image)













