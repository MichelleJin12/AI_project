import cv2
import numpy as np
import os
from redis import Redis
cli = Redis('localhost')
share = 6
cli.set('share_rec', share)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0
count = 0

# names related to ids: example ==> loze: id=1,  etc
# 이런식으로 사용자의 이름을 사용자 수만큼 추가해준다.
names = ['None', 'jaewon']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

name_list = []
if cam.isOpened() == False:  # 카메라 생성 확인
    exit()

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])  # gray[y:y+h,x:x+w] : 얼굴 부분만 가져오기
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (100 - confidence > 30):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    if id == "unknown":
        count += 1
        print(count)
        if count > 10:
            share = 1
            cli.set('share_rec', share)
    id = " "
    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video

    if k == 27:
        break

print("\n [INFO] Exiting Program and cleanup stuff")
# print(name_list)
cam.release()
cv2.destroyAllWindows()