
# Import package

import cv2
import numpy as np
from os import makedirs , listdir
from os.path import isfile , join , isdir


# function - Crop face from photo


def faceCropping(img):
    faceClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    toGray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    faces = faceClassifier.detectMultiScale(toGray , 1.3 , 5)

    if faces is():
        return None
    
    for(x,y,w,h) in faces:
        croppedFace = img[y : y + h , x : x + w]
        print('working...')
        return croppedFace


# function - Taking pictures with the Raspberry Pi camera


def pictureCollecting(name):
    faceDirs = 'faces/'
    
    if not isdir(faceDirs + name):
        makedirs(faceDirs + name)
    
    cap = cv2.VideoCapture(-1)
    cap.set(3, 640)
    cap.set(4, 480)
    count = 0
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('video',frame)
        if faceCropping(frame) is not None:
            count += 1
            face = cv2.resize(faceCropping(frame) , (200 , 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            saveFile = faceDirs + name + '/cropped (%d).jpg' % count
            cv2.imwrite(saveFile , face)
            
            cv2.putText(face , str(count) , (50,50) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0,255,0) , 2)
            cv2.imshow('Face' , face)
    
        else:
            print("no face")
            pass
    
        if cv2.waitKey(1) == 13 or count == 10:
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Done.')


# Face data training and modeling generation


def modelTraining(name):
    
    if not isdir('faces/models'):
        makedirs('faces/models')
        
    imgPath = 'faces/' + name + '/'

    fileLst = [f for f in listdir(imgPath) if isfile(join(imgPath , f))]

    trainingModel , labels = [] , []

    for i , files in enumerate(fileLst):
        imgPaths = imgPath + fileLst[i]
        images = cv2.imread(imgPaths , cv2.IMREAD_GRAYSCALE)
    
        if images is None:
            continue
    
        trainingModel.append(np.asarray(images , dtype = np.uint8))
        labels.append(i)
    
    if len(labels) == 0:
        print("no data.")
        exit()
        
    labels = np.asarray(labels , dtype = np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(trainingModel) , np.asarray(labels))
    model.save('faces/models/' + name + ".yml")
    print("Done.")


# main function


if __name__ == "__main__":
    print("main")