
# Import package


import cv2
from os import listdir, makedirs
from os.path import isdir
import time


# A function for the camera to recognize a face


def faceTracker(img , size = .5):
    faceClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    faces = faceClassifier.detectMultiScale(gray , 1.3 ,5)
    if faces is():
        return img , []
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x , y) , (x + w , y + h),(0,255,255),2)
        roi = img[y : y + h, x : x + w]
        roi = cv2.resize(roi, (200 , 200))
    return img , roi


# Face data training and modeling generation


def faceRecognition():
    
    modelDic = {}
    cap = cv2.VideoCapture(-1)
    modelPath = "faces/models/"
    if not isdir(modelPath):
        makedirs(modelPath)
    modelList = listdir(modelPath)
    startTime = time.time()
    
    for lst in modelList:
        model = cv2.face.LBPHFaceRecognizer_create()
        model.read(modelPath + lst)
        key = lst[:-4]
        modelDic[key] = model

    while(True):
        endTime = time.time()
        ret, frame = cap.read()
        image , face = faceTracker(frame)
        try:
            minScore = 999
            minScoreName = ""
            
            face = cv2.cvtColor(face , cv2.COLOR_BGR2GRAY)
            
            for key, model in modelDic.items():
                result = model.predict(face)
                if minScore > result[1]:
                    minScore = result[1]
                    minScoreName = key
                    
            if result[1] < 500:
                confidence = int(100 * (1 - (result[1]) / 300))
                displayString = str(confidence) + '% Confidence it is' + minScoreName
            cv2.putText(image,displayString,(100 , 120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
            if confidence > 75:
                cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', image)
                cap.release()
                cv2.destroyAllWindows()
                return minScoreName
            else:
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Cropper', image)
        except:
            cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Face Cropper', image)
            pass
        if (cv2.waitKey(1) == 13) or ((endTime - startTime) > 10):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    return 0


# main function


if __name__ == "__main__":
    faceRecognition()