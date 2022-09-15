import face_recognition
import os
import cv2

path=r"D:\College Projects\Look Like\images"

images=[]
classes=[]
encoding_list=[]
def Face_Encoding():

    for i in os.listdir(path):
        image=cv2.imread(os.path.join(path,i))
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        images.append(image)
        classes.append(os.path.splitext(i)[0])
        encoding_list.append(face_recognition.face_encodings(image)[0])
    return images,classes,encoding_list 

# while 1:
#     url=input("Enter URL: ")
#     print("Loading.....")
#     os.system("cls" if os.name=="nt" else "clear")
#     if url=='q':
#         exit()
#     else:
#         img=req.urlretrieve(url,"image.png")
#         img=cv2.imread("image.png")
#         img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#         face_encode=face_recognition.compare_faces(encoding_list,face_recognition.face_encodings(img)[0])
#         distance=face_recognition.face_distance(encoding_list,face_recognition.face_encodings(img)[0])

#         for x in range(len(face_encode)):
#             if face_encode[x]:
#                 print(classes[x])
#         a=np.argmin(distance)
#         print(classes[a])

path=r"D:\College Projects\Look Like\images"
a=1
for i in os.listdir(path):
        image=cv2.imread(os.path.join(path,i))
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        name=os.path.splitext(i)[0]
        id=str(a)
        a+=1
        encoding_list.append(face_recognition.face_encodings(image)[0])


image=cv2.imread(r"D:\College Projects\Look Like\images\brie larson - captain marvel.jpg")
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
encoding_data=face_recognition.face_encodings(image)[0]

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Attendence"]

user_collection =mydb["Users"]
encoding_data_collection = mydb["Encoding_data"]

user_data={
  "ID":"123",
  "Name":"BRIE LARSON",
  "Department":"Avenger",
  "Designation":"Captain Marvel"
}
# user_collection.insert_one(user_data)
ref_id=user_collection.find({},{ "ID":"123" })

enc_data={
  "ref":ref_id[0]["ID"],
  "enc":list(encoding_data)
}

# encoding_data_collection.insert_one(enc_data)
print("Successfully connected to Database...")

# images,classes,encoding_list=Face_Encoding()

data=encoding_data_collection.find({'ref':"123"})
face=copy.deepcopy(face_recognition.compare_faces([data[0]['enc']],face_recognition.face_encodings(image)[0]))
print(face)