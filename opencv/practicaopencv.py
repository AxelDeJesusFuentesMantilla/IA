import cv2
import numpy as np

img = cv2.imread(r"C:\Users\akino\Downloads\civic.jpeg",1)
imgn = np.zeros(img.shape[:2], np.uint8)
print(img.shape)
b,g,r = cv2.split(img)
imgb=cv2.merge([b,imgn,imgn])
imgg=cv2.merge([imgn,g,imgn])
imgr=cv2.merge([imgn,imgn,r])

img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img4 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#cv2.imshow('salida',img)
#cv2.imshow('salida2',img2)
#cv2.imshow('salida3',img3)  

cv2.imshow('salida',imgb)
cv2.imshow('salida2',imgg)
cv2.imshow('salida3',imgr)
    

cv2.waitKey(0)
cv2.destroyAllWindows()