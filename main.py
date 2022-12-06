import os
import cv2
import numpy as np
import shutil
from tools.inference import *

detection_rate = 5
video_path = ""

def get_normal_frames():
    count = 0
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        frame_id = cap.get(1)
        ret, frame = cap.read()
        if ret is not True:
            break
        if frame_id % 5 == 0:
            file_name = 'temp/retrain/normal/%s.jpg' % count;count+=1
            cv2.imwrite(file_name, frame)
            if count == 2: break
    cap.release()

def frames():
    count = 0
    video = cv2.VideoCapture(video_path)
    frame_rate = video.get(5)

    while video.isOpened():
        frame_id = video.get(1)
        ret, frame = video.read()
        if ret is not True:
            break
        if frame_id % (frame_rate * detection_rate) == 0:
            file_name = 'temp/frames/%02d.jpg' % count;count+=1
            cv2.imwrite(file_name, frame)
    video.release()

def make_dirs():
    parent_dir = 'temp'
    if os.path.exists(parent_dir): shutil.rmtree(parent_dir)
    os.mkdir(parent_dir)
    folders = ['frames', 'retrain', 'retrain/normal', 'retrain/anomaly']
    for folder in folders:
        dir = os.path.join(parent_dir, folder)
        os.mkdir(dir)
    
    blank_image = np.zeros((100, 100, 3), np.uint8)
    cv2.imwrite('temp/retrain/anomaly/blank.jpg', blank_image)

def get_parameters():

    global video_path
    video_path = input('Enter the video path: ')

    global detection_rate
    detection_rate = int(input('Choose detection rate (default 5): ') or "5")

def generate_output(predictions):

    video_segment = 0
    is_anomalous = []

    for frame in predictions:
        pred_score = (frame["pred_scores"][0]).item()

        print("%d - %d second of input sequence is " %
        (detection_rate * video_segment, detection_rate * (video_segment+1)), end = '');video_segment+=1

        if pred_score > 0.2:
            print("anomalous.")
            is_anomalous.append(True)
        else:
            print("normal.")
            is_anomalous.append(False)

    video = cv2.VideoCapture(video_path)
    frame_rate = video.get(5)

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)

    result = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)

    while video.isOpened():
        frame_id = video.get(1)
        ret, frame = video.read()
        if ret is True:

            current_video_segment = int(frame_id / (frame_rate * detection_rate))

            if is_anomalous[current_video_segment]:

                frame = cv2.putText(
                    img = frame,
                    text = 'ANOMALY',
                    org = (12, 30),
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale = 1.0,
                    color = (0, 0, 255),
                    thickness = 3
                    )

            result.write(frame)
        else: break

    video.release()

if __name__ == "__main__":
    
    os.system('cls')
    make_dirs()
    get_parameters()
    frames()
    get_normal_frames()
    retrain()
    predictions = infer()
<<<<<<< HEAD
    generate_output(predictions)
=======
    generate_output(predictions, video)
    
>>>>>>> 12159957e54621488100fa3db28a4c9326536b5c
