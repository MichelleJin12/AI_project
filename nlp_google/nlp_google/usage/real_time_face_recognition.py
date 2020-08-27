#!/usr/bin/env python
# coding: utf-8



import argparse
import sys
import time

import cv2
import os
import face
import datetime

import classifier
from redis import Redis
cli = Redis('localhost')
share = 0
# face.prob*100

window_name = "Real_Time_Facial_Recognition"

def add_overlays(frame, faces, frame_rate,count):
    if faces is not None:
        for face in faces:

            face_bb = face.bounding_box.astype(int)
            
            cv2.rectangle(frame,
                          (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), 
                          (0, 255, 0), 2)
            # print(abs(face_bb[0] - face_bb[2]))
            if abs(face_bb[0] - face_bb[2])>=140:
                count += 1
#             print(frame.shape)    # (240, 320, 3)
            if face.name is not None:
                if max(face.prob[0]*100) > 90:  # 90% 보다 높으면 이름과 확률 출력
                    cv2.putText(frame, "{} {}%".format(face.name, max(face.prob[0]*100)), (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)
                else:                           # 아니면 unknown 출력
                    cv2.putText(frame, "{}".format('unknown'), (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)
    return frame, count
def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='Enable some debug outputs.')
    parser.add_argument('--model', help='Model to use.', required=True)
    parser.add_argument('--classifier', help='Classifier to use.', required=True)
    return parser.parse_args(argv)


args = parse_arguments(['--model', '/models/20180402-114759', '--classifier', '/models/datasets_classifier.pkl'])


frame_interval = 30  # Number of frames after which to run face detection
fps_display_interval = 5  # seconds
frame_rate = 0
frame_count = 0
face_flag = 0
count = 0
temp = 0

if args.debug:
    print("Debug enabled")
    face.debug = True

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
video_capture.set(cv2.CAP_PROP_FPS, 30)

facenet_model_checkpoint = os.path.dirname(__file__) + args.model
classifier_model = os.path.dirname(__file__) + args.classifier
face_recognition = face.Recognition(facenet_model_checkpoint, classifier_model, min_face_size=20)
start_time = time.time()
cli.set('share_rec', share)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if ret == 0:
        print("Error: check if webcam is connected.")
        pass

    faces = face_recognition.identify(frame)


    if (frame_count % frame_interval) == 0:
        # Check our current fps
        end_time = time.time()
        if (end_time - start_time) > fps_display_interval:
            frame_rate = int(frame_count / (end_time - start_time))
            start_time = time.time()
            frame_count = 0

    new_frame,count = add_overlays(frame.copy(), faces, frame_rate, count)
    if count > 20:
        face_flag = 1
        # 여기에서 보내줘야된다.
        cli.set('share_rec', face_flag)
        cli.set('share_img', frame.tobytes())
        if frame_count == 0 :
            temp = 89
        else:
            temp = frame_count - 1
        count = 0

    if face_flag == 1:
        if frame_count == temp:
            face_flag = 0
            #여기서 다시 보내줘야한다.
            cli.set('share_rec', face_flag)


    frame_count += 1
    cv2.imshow(window_name, new_frame)
    # print(frame.shape)
    keyPressed = cv2.waitKey(1) & 0xFF
    if keyPressed == 27: # ESC key
        break
    elif keyPressed == 13: # ENTER key
        cv2.imwrite(window_name + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg", frame);
        print('Screenshot saved!')


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

    