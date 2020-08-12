code 2

the code below is used for the process of detection of shots in the video and pro

import cv2

import numpy as np
import math
import easygui as eg# easygui is the module used for creating the GUI

v = eg.fileopenbox(msg='Select the video which you would like to Annotate', title='VIDEO ANNOTATION', default='*', filetypes='*.avi')# dialog box asks which video you want annotate
cap = cv2.VideoCapture(v)
print(v)

fc = cap.get(7)# no of frames in the video
fps = cap.get(5)# fps of the video

fc = int(math.floor(fc+1))  #converting float to integer 
fr = range(1,fc-1,2)  #range does no accept float

y=0.0#initialsing y, used for comparing with the shot detected time

vt=fc/fps#total time of the video

a = eg.enterbox(msg='Provide the names for the annotation files', title='', default='', strip=True, image=None, root=None)#give a name for the annotation files in which keywords will be saved
nk=0                  #no of key frames

l=open('C:\\shripadproject\\listofannotationfiles','a+')#creating a file so as to record the names of annotation files,file opened in append and read mode 'a+'
l.write('\n')
l.write(a)
l.close()


Time='C:\\shripadproject\\'+a+'time'
Annotation = 'C:\\shripadproject\\'+a+'annotation'
f = open(Time, 'w')  #recording annotation time
g = open(Annotation, 'w')  #recording annotation
f.write(v)#writing the location of the file being annotated
f.write('\n')
g.write(v)#writing the location of the file being annotated
g.write('\n')

for i in  fr:
   if i==1: #execute if its the first frame

       ret,img1 = cap.read()#read the first frame
       ret,img = cap.read()
       ret,img2 = cap.read()#read the third frame and skip the second frame by using the above code
       
       mask = np.zeros(img1.shape[:2], np.uint8)  #making mask image of the size of input image amd making all pixels zero
       mask[ 90:270,160:480] = 255    #making the range of pixel for mask,first verical and then horizontal,equal to white
       
       histB1 = cv2.calcHist([img1],[0],mask,[256],[0,256])#calculation of histogram for blue colour for 1st frame
       histG1 = cv2.calcHist([img1],[1],mask,[256],[0,256])#calculation of histogram for green colour for 1st frame
       histR1 = cv2.calcHist([img1],[2],mask,[256],[0,256])#calculation of histogram for red colour for 1st frame
       
       histB2 = cv2.calcHist([img2],[0],mask,[256],[0,256])#calculation of histogram for blue colour for 3rd frame
       histG2 = cv2.calcHist([img2],[1],mask,[256],[0,256])#calculation of histogram for blue colour for 3rd frame
       histR2 = cv2.calcHist([img2],[2],mask,[256],[0,256])#calculation of histogram for blue colour for 3rd frame

       valueB = cv2.compareHist(histB1,histB2,0)#comparison of histograms gives a correlation value of the 2 histograms
       valueG = cv2.compareHist(histG1,histG2,0)
       valueR = cv2.compareHist(histR1,histR2,0)

       
   elif(fc-1-i)>2:
        frei=str(i+2)
        histB1=histB2
        histG1=histG2
        histR1=histR2

        
        ret,img = cap.read()
        ret,img2 = cap.read()#reading the odd frames skipping every consecutive frame

        histB2 = cv2.calcHist([img2],[0],mask,[256],[0,256])
        histG2 = cv2.calcHist([img2],[1],mask,[256],[0,256])
        histR2 = cv2.calcHist([img2],[2],mask,[256],[0,256])

        valueB = cv2.compareHist(histB1,histB2,0)
        valueG = cv2.compareHist(histG1,histG2,0)
        valueR = cv2.compareHist(histR1,histR2,0)

   value = (valueB*valueB+valueG*valueG+valueR*valueR)/3# average value of the three compared values
   #frei=float(frei)
   frei=float(i+2)
   #print(i)
   #print(value)
   x=(frei)/fps
   if value < 0.64:#detecting a new shot if not crossing threshold
               if (x-y)>1.0 or x<1.0:#time between two detected shots should be greater then one second 
                   if (vt-x)>1.0:#last shot detected should last for atleast one second
                       y=x
                       x=str(x)
                       if nk>0:#new time and annotation has to be written on a new line 
                           f.write('\n')
                           g.write('\n')
                       nk=nk+1
                       nk=str(nk)
                       z='C:\\shripadproject\\'+a+nk+'.png'#location where the first frame of every shot is to be stored
                       print(z)
                       cv2.imwrite(z,img2)#save the first frame of every shot detected
                       nk=int(nk)
                       annotate = eg.enterbox(msg='Provide annotation to the shot ', title='New shot detected ', default='', strip=True, image=z, root=None)#ask the programmer to annotate the detected shot
                       f.write(x)#write the time in time file
                       g.write(annotate)# write the annotation in the annotation file
                       
cap.release()
f.close()
g.close()
eg.msgbox("All the shots are detected and annotated")#after all the shots are detected and annotated display this message  
n=open('C:\\shripadproject\\'+a+'Number', 'w')#create a number file to store the number of shots detected
nk=str(nk+1)
n.write(nk)#write the number of shots detected
n.close()

