# video_decoder.py - decodes video into frames that can be understood by vision model

import cv2
import os

def decode_video_general(video_path:str):
    
    frames_filepaths = []
    video = cv2.VideoCapture(video_path)
    i = 1

    while True:
        success, frame = video.read()
        time_ms = video.get(cv2.CAP_PROP_POS_MSEC)
        
        if not success:
            print(f'decode_video_general: Failed to retrieve frame from video at {time_ms/1000} seconds.')
            break

        filepath = f'C:/Users/alexf/Documents/CSC/mma_coach/backend/video/frames_general/frame{i}.jpg'
        frames_filepaths.append(filepath)
        if not os.path.exists(f'C:/Users/alexf/Documents/CSC/mma_coach/backend/video/frames_general/frame{i}.jpg'):
            cv2.imwrite(filepath,frame)

        video.set(cv2.CAP_PROP_POS_MSEC, (3000 + time_ms))
        i += 1

    video.release()
    print('General frames saved successfully')

    return frames_filepaths

def decode_video_specific(video_path:str,start_pos, end_pos):

    frames_filepaths = []
    video = cv2.VideoCapture(video_path)
    video.set(cv2.CAP_PROP_POS_MSEC, start_pos)
    i = 1

    skip_amount = float(end_pos - start_pos) / 50 # i want about 50 frames, takes about 4-8 minutes for model to process on my laptop
    time_ms = video.get(cv2.CAP_PROP_POS_MSEC)


    while True:
        success, frame = video.read()

        if not success:
            print(f'decode_video_specfic: Failed to retrieve frame from video at {time_ms/1000} seconds. (Or last frame was met)')
            break
        if time_ms >= end_pos:
            break
        
        filepath = f'C:/Users/alexf/Documents/CSC/mma_coach/backend/video/frames_specific/frame{i}.jpg'
        frames_filepaths.append(filepath)
        if not os.path.exists(f'C:/Users/alexf/Documents/CSC/mma_coach/backend/video/frames_specific/frame{i}.jpg'):
            cv2.imwrite(filepath,frame)

        time_ms += skip_amount

        video.set(cv2.CAP_PROP_POS_MSEC, time_ms)
        i += 1

    video.release()
    print('Specific frames saved successfully.')
    
    return frames_filepaths


