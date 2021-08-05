import cv2
import numpy as np
import os

'''
flipping a video upside down and left to right. it is necessary because the camera in the app
flips the video when its taking it
'''
def flip_video(filename):
    cap = cv2.VideoCapture(filename)
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    frame_rate = 29
    resulution = (int(cap.get(3)), int(cap.get(4)))
    video_output = cv2.VideoWriter('flipped.mkv', codec, frame_rate, resulution)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        flipped_image = np.flipud(np.fliplr(frame))
        video_output.write(flipped_image)
    cap.release()
    video_output.release()
    cv2.destroyAllWindows()
    os.remove(filename)
    os.rename('flipped.mkv', filename)
    