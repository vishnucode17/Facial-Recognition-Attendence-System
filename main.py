import numpy as np
import cv2
import face_recognition
import os
import copy
# from face_encoding import Face_Encoding
from urllib import request as req
import pymongo
import datetime
import time
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client['Attendence']
user_collection=db['Users']
enc_collection=db['Encoding_data']
attendence_collection=db['attendence']

user_schema={
  "USN":"",
  "Name":"",
  "Department":"",
}

enc_schema={
  "USN":"",
  "encoding":"",
}

attendence_schema={
  "USN":"",
  "timestamp":""
}
vid = cv2.VideoCapture(0)

encoding_list=[np.array(x['encoding']) for x in enc_collection.find()]
names=[(x["Name"],x["USN"]) for x in user_collection.find()]

while True:
  ret, frame = vid.read()
  cv2.imshow('frame', frame)
  img=np.array(frame)
  try:  
    img_face_encoding=face_recognition.face_encodings(img)[0]
    face_encode=face_recognition.compare_faces(encoding_list,img_face_encoding)
    if True not in face_encode:
      print("Face not matched!!!")
      choice=input("Enter any key to register the face or press 'q' to exit")
      if choice!='q':
        usn=input("Enter USN: ")
        name=input("Enter name: ")
        department=input("Enter department: ")
        print("Stay still....Capturing image in ",end=" ")
        for x in range(1,4):
          print(4-x)
          time.sleep(1)
        img_encoding=face_recognition.face_encodings(img)[0]
        user_values=[usn,name,department]
        enc_values=[usn,list(img_encoding)]
        user_schema.update(dict(zip(user_schema.keys(),user_values)))
        enc_schema.update(dict(zip(enc_schema.keys(),enc_values)))
        user_collection.insert_one(user_schema)
        enc_collection.insert_one(enc_schema)
        print("Data saved succesfully..")
    else:
      for x in range(len(face_encode)):
        if face_encode[x]:
          print(f"Welcome {names[x][0]}")
          usn=names[x][1]
          try:
            time_stamp=attendence_collection.find({"USN":usn})[0]['timestamp']
            date_value=time_stamp.split(',')[0]
            date_value=date_value.split('/')
            Day=int(date_value[1])
            Month=int(date_value[0])
            Year=int(date_value[2])
            now=datetime.datetime.now()
            if now.year==Year and now.month==Month and now.day==Day:
            
              print("Attendence Already exists")
              break
          except:
            print("Welcome new user")
          
          timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
          attendence_values=[usn,timestamp]
          attendence_schema.update(dict(zip(attendence_schema.keys(),attendence_values)))
          attendence_collection.insert_one(attendence_schema)
          print("Attendence taken succesfully!")
  except:
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
