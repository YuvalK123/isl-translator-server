from flask_ngrok2 import run_with_ngrok
from flask import Flask, jsonify, request
import json
import firebase_controller as fbc
import video_preprocessing as vp
import cv2
import mediapipe as mp
import numpy as np
import os

'''
takes a video and creating landmarks video out of it
'''
def process_video(filename, expression):
    mp_draw = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    cap = cv2.VideoCapture(filename)

    animation = f'animation_{expression}.mp4'
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    frame_rate = 29
    resulution = (int(cap.get(3)), int(cap.get(4)))

    video_output = cv2.VideoWriter(animation, codec, frame_rate, resulution)

    with mp_holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
        while cap.isOpened():

            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)

            empty_img = np.zeros(frame.shape, dtype=np.uint8)
            mp_draw.draw_landmarks(
                empty_img, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
            mp_draw.draw_landmarks(
                empty_img, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            mp_draw.draw_landmarks(
                empty_img, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            mp_draw.draw_landmarks(
                empty_img, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            video_output.write(empty_img)
        cap.release()
        video_output.release()
        cv2.destroyAllWindows()
    return animation



app = Flask(__name__)
run_with_ngrok(app)


'''
handles users https requests from the app:
1. receve a request with a name of a video file
2. downloading that video from firebase
3. turning the video upside down
3. extracting landmarks
4. creating a video out of the landmarks
5. uploading both videos to firebase
6. returning https response
'''
@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if (request.method == 'POST'):
        # loading https post request data
        request_data = json.loads(request.data.decode('utf-8'))
        uid = request_data['uid']
        filename = request_data['filename']
        expression = request_data['expression']

        # dounloading video from fire base
        print('downloading video')
        fbc.download(f'live_videos/{uid}/{filename}', filename)

        # flipping the video upside down
        vp.flip_video(filename)

        # creating landmark video
        print('video downloaded.\nproccesing...')
        animation_name = process_video(filename, expression)

        # uploading animation and flipped video
        print('proccess done.\nuploading animation...')
        fbc.upload(f'animation_openpose/{uid}/{expression}.mp4', animation_name)
        fbc.upload(f'live_videos/{uid}/{filename}', filename)

        # removeing videos from local folder
        os.remove(animation_name)
        os.remove(filename)

        print('upload completed.')

        return 'success'


if __name__ == '__main__':
    app.run()
