import numpy as np
import cv2
import easygui as eg
import sys
import enchant
from matplotlib import pyplot as plt

def videoplay(timee,set):#function used to play the video, input to it is the location of video file and time from which it has to be opened
    import math
    import time as ti
    t=float(timee)
    
    set=str(set)
    set=set.split()
    set=set.pop()
    cap = cv2.VideoCapture(set)

    fc = cap.get(7)# number of frames in video
    fc = int(math.floor(fc+1))#converting float to integer
    fps = cap.get(5)#frame rate of the video
    print('fps is',fps)

    cap.set(0,t*1000)#set the time from where video has to be opened(time has to specified in milliseconds hence mutiplied by 1000)
    f= (t/fps)*fc#initialse the frame counter based on the time retrieved
    f=int(f)
    framespersec =int(fps)
    while(cap.isOpened()):#check whether video can be opened
                        ret,frame = cap.read()
                        cv2.imshow('Video',frame)
                        f=f+1
                        if cv2.waitKey(framespersec)& 0xFF == ord('c') or f == fc-1 :#check whether the last frame is displayed or user has pressed key "c" is closed
                            break
    ti.sleep(0.5)
    
    cap.release()
    cv2.destroyAllWindows()
    

def videoindexing(input):# indexing  function used to find the right time for which user query matches with the annotation,input to the function is the user query
    import math
    import time as ti
    import re

    a=[]
    l=open('C:\\shripadproject\\listofannotationfiles','a+')#open the file containing llist of all annotated videos
    list=l.read()
    list=list.split()
    print(list)
    for i in range(len(list)):# to find out the videos which match with the query
        j='C:\\shripadproject\\'+list[i]+'annotation'
        print(j)
        c=open(j,'r')
        m=re.search(input,c.read())
        print('m is',m)
        if m!=None:
            a.append(list[i])#append the names of video files match the query to a list
            c.close()
    if a==[]:
        eg.msgbox("No relevant content found")#if there are no matching videos
    else:
        a=a.pop(0)
    a=str(a)
    n=open('C:\\shripadproject\\'+a+'Number', 'r')
    nk=n.readline()#reading no of key frames
    f=open('C:\\shripadproject\\'+a+'time','r')
    t=f.readline()
    g=open('C:\\shripadproject\\'+a+'annotation','r')
    s=g.readline()#read the location of video file
    print(s)

    nk=int(nk)
    fn = range(1,nk)
    print(fn)
    
    timee=[]# list of times for which annotation and input can match, useful in case there are more than one match
    w=0
    morethanoneresults=[]
    
    for i in fn:
        annotation=g.readline()
        #annotation=annotation.split()
        o=f.readline()
        z=re.search(input,annotation)
        if z!=None:
            o=float(o)
            timee.append(o)#appending all the times to the list for which annotations are matching
            w+=1
            print('w is',w)
            morethanoneresults.append(i)#to record which shots are matching with the query
            print('match')
            #print(time)
            print(annotation)
              
    if timee==[]:
        eg.msgbox("No relevant content found")
    else:
        if w>1:
            print('morethanoneresults',morethanoneresults)
            print('range(0,w)',range(0,w))
            for i in range(0,w):
                print('i is',i)
                q=morethanoneresults.pop()
                print(q)
                k=str(q)
                g='C:\\shripadproject\\wildlife'+k+'.png'
                img=cv2.imread(g,1)
                print(g)
                b=str(i)
                cv2.imshow(b,img)#in case of more than one results show the first frames of the matching shots 
            w=str(w)
            inm = eg.enterbox(msg='There are '+w+' relevant results. Please indicate which one you want to view ', title='', default='', strip=True, image=None, root=None)
            #print(inputmorethanone)
            inm =int(inm)
            for i in range(0,inm+1):
                timeepop=timee.pop()
            cv2.destroyAllWindows()
            videoplay(timeepop,s)
        else:
            videoplay(timee.pop(0),s)
            

    
    
input = eg.enterbox(msg='ENTER THE QUERY ABOUT THE CONTENT\nYOU CAN CLOSE THE VIDEO ANYTIME BY PRESSING "c"', title=' ', default='', strip=True, image='C:\shripadproject\Computer.jpg', root=None)
if input == None:
   eg.msgbox("Please provide an input if you wish to continue")
   input = eg.enterbox(msg='ENTER THE QUERY ABOUT THE CONTENT\nYOU CAN CLOSE THE VIDEO ANYTIME BY PRESSING "c"', title=' ', default='', strip=True, image='C:\shripadproject\Computer.jpg', root=None)
else:
   x = input.split()
   xwords=''
   s=0
   d = enchant.Dict("en_US")
   for i in range(len(x)):
       y = d.check(x[i])#check whether the word  is spelled correctly
       if y == True:
           j=str(x[i])
           xwords+=j
       if y == False and (d.suggest(x[i])!=[]):# if there is spelling mistake present and if there are suggestions for the mistake
           n=str(d.suggest(x[i]))
           xwords+=n
           s=1
       xwords+='\n'

   if y == False:
           if s==1:
               u='It seems there are some spelling errors. Please check the suggestions provided\n\n'
           else:
               u='It seems there are some spelling errors.\n\n'
           xwords = str(xwords)
           input = eg.enterbox(msg=u+xwords, title='Spelling Error', default='', strip=True, image=None, root=None)
       
   x=input.split()        
   print(x)
   videoindexing(input)

