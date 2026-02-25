# video_decoder.py - decodes video into frames that can be understood by vision model

import cv2
import os

def decode_video(video_path:str):
    frames_filepaths = []

    video = cv2.VideoCapture(video_path)
    i = 1

    while True:
        success, frame = video.read()
        time_ms = video.get(cv2.CAP_PROP_POS_MSEC)
        
        if not success:
            print(f'Failed to retrieve frame from video at {time_ms/1000} seconds.')
            break
        filepath = f'C:/Users/alexf/Documents/CSC/mma_coach/backend/video/frames/frame{i}.jpg'
        frames_filepaths.append(filepath)
        if not os.path.exists(f'C:/Users/alexf/Documents/CSC/mma_coach/backend/video/frames/frame{i}.jpg'):
            cv2.imwrite(f'C:/Users/alexf/Documents/CSC/mma_coach/backend/video/frames/{filepath}',frame)

        video.set(cv2.CAP_PROP_POS_MSEC, (3000 + time_ms))
        i += 1

    video.release()

    print('frames saved successfully')
    return frames_filepaths