import cv2 as cv 
import numpy as np 
import os

dataSet = 'C:\\Users\\akino\\OneDrive\\Documentos\\Tareas TECNM\\Semestre 9\\IA\\repo\\IA\\HaarCascade\\recorte'
faces  = os.listdir(dataSet)
print(faces)

labels = []
facesData = []
label = 0 
for face in faces:
    facePath = dataSet+'/'+face
    for faceName in os.listdir(facePath):
        labels.append(label)
        facesData.append(cv.imread(facePath+'/'+faceName,0))
    label = label + 1
#print(np.count_nonzero(np.array(labels)==0)) 
faceRecognizer = cv.face.FisherFaceRecognizer_create()
faceRecognizer.train(facesData, np.array(labels))
path= 'C:\\Users\\akino\\OneDrive\\Documentos\\Tareas TECNM\\Semestre 9\\IA\\repo\\IA\\HaarCascade\\xml\\'
faceRecognizer.write(f'{path}FisherFace.xml')
