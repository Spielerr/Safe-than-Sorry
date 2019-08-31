# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 20:19:26 2019

@author: manum
"""

import face_recognition
import numpy as np
import pandas as pd
import cv2 as cv


def LoadDatabase(FilePath):
    images=list()
    AccNo=list()
    Database=pd.read_csv(FilePath)
    dataFrame=pd.DataFrame(Database)
    images=dataFrame.Image
    AccNo=dataFrame.AccNo
    for i in range(len(images)):
        images[i]=face_recognition.load_image_file(images[i])
        images[i]=face_recognition.face_encodings(images[i])[0]
    return images,AccNo
def LoadImage(Image):
    image=face_recognition.load_image_file(Image)
    encoded=face_recognition.face_encodings(image)[0]
    return encoded
def readVideo(known_encoding,AccNo):
    face_encodings,face_locations,face_names=list(),list(),list()
    process_frame=True
    while True:
        video_capture=cv.VideoCapture(0)
        ret,frame=video_capture.read()
        small_frame=cv.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame=small_frame[:,:,::-1]
        if process_frame:
            face_locations=face_recognition.face_locations(rgb_small_frame)
            face_encodings=face_recognition.face_encodings(rgb_small_frame,face_locations)
            
            face_names=[]
            for face_encoding in face_encodings:
                matches=face_recognition.compare_faces(known_encoding,face_encoding)
                name="Unknown"
                face_distance=face_recognition.face_distance(known_encoding,face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = AccNo[best_match_index]

                face_names.append(name)
                
        process_frame=not process_frame
    return face_names
                
                
def Fraud(Transaction_Acc_no,FilePath):
    images,AccNO=LoadDatabase(FilePath)
    face_Name=readVideo(images,AccNO)
    if Transaction_Acc_no in face_Name:
        return True
    return False
    
              
                
                
                
                
                
                
                
                
                
                
                