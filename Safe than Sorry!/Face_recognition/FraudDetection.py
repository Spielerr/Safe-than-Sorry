# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 20:19:26 2019

@author: manum
"""

import face_recognition
import numpy as np
import pandas as pd
import cv2 as cv
import imutils


def LoadDatabase(FilePath):
    images=list()
    encoding=list()
    loaded_image=list()
    AccNo=list()
    Database=pd.read_excel(FilePath)
    dataFrame=pd.DataFrame(Database)
    images=dataFrame.Image
    AccNo=dataFrame.AccNo
    dim=(1920,1920)
    angle270 = 270
    for i in range(len(images)):
        loaded_image.append(face_recognition.load_image_file(images[i]))
        w,h,depth=loaded_image[i].shape
        if(w!=1920 or h!=1920):
            loaded_image[i]=imutils.rotate_bound(loaded_image[i],angle270)
            loaded_image[i]=cv.resize(loaded_image[i],dim,cv.INTER_AREA)
        encoding.append(face_recognition.face_encodings(loaded_image[i]))
    return encoding,AccNo


def LoadImage(Image):
    image=face_recognition.load_image_file(Image)
    encoded=face_recognition.face_encodings(image)[0]
    return encoded


def readVideo(known_encoding):
    face_encodings,face_locations=list(),list()
    count=0
    process_frame=True
    while True:
        video_capture=cv.VideoCapture(0)
        ret,frame=video_capture.read()
        small_frame=cv.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame=small_frame[:,:,::-1]
        if process_frame:
            face_encodings=face_recognition.face_encodings(rgb_small_frame,face_locations)
            for face_encoding in face_encodings:
                matches=face_recognition.compare_faces(known_encoding,face_encoding,0.8)
                #best_match_index = np.argmin(face_distances)
                if np.any(matches):
                    return True
        cv.imshow('Video', frame)
        count+=1
        if count==5:
            break
        # Hit 'q' on the keyboard to quit!
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv.destroyAllWindows()
    return False
def LoadAccImages(TransactionAccNo,FilePath):
    dataframe=pd.read_csv(FilePath)
    AccNo,images=list(),list()
    AccNo=dataframe["AccNo"]
    index_of_account=0
    for i in range(len(AccNo)):
        if int(AccNo[i])==TransactionAccNo:
            index_of_account=i
            break;
    #index_of_account=AccNo.index(TransactionAccNo)
    images=dataframe["Image"]
    image=images[index_of_account]
    image=image.split("|")
    image_encoding=list()
    for i in image:
        j=face_recognition.load_image_file(i)
        image_encoding.append(face_recognition.face_encodings(j))
    return image_encoding
    
                
def Fraud(Transaction_Acc_no,FilePath):
    image_encoding=LoadAccImages(Transaction_Acc_no,FilePath)
    #images,AccNO=LoadDatabase(FilePath)
    return readVideo(image_encoding)
    
              
                
                
                
                
                
                
                
                
                
                
                