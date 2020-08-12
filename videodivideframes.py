code no 1
The code is used for extracting and saving the frames in a folder.The default location is C:\shripadproject\Frames 

import numpy as np #importing the numpy module,  it is required for the array manipulation

import cv2#importing the opencv module into the python so as to do image processing 

import math#importing mathematics module for math operations

cap = cv2.VideoCapture('C:\\Users\\Administrator\\Desktop\\shripadproject\\Chennai1.avi')# video capture object for the specified object for accesing various properties of the video
f=0#initialise the frame count

fc = cap.get(7)#is used to access the total number of frames 

print(cap.get(5))#prints the frame rate of the video


print fc#prints the number of frames in video

fc = int(math.floor(fc+1))#converting float to integer 
fr = range(1,fc)#range does no accept float
if(cap.isOpened()):# checking whether it is possible to open the video
    for i in  fr:
       ret, frame = cap.read()Read the frames of video
       fra= str(i) #converting numbers to string
       fra= 'Chennai1'+fra 
       fram= fra+'.png'
       framee ='C:\\Users\\Administrator\\Desktop\\shripadproject\\Frames\\'+fram # adding the correct location for storing the frames
       #print i
       cv2.imwrite(framee,frame)#save the frame in the location specified above
       f=f+1
cap.release()
