# video_decoder.py - decodes video into frames that can be understood by vision model

import cv2
import os
import statistics

def decode_video_general(video_path:str):
    
    frames_filepaths = []
    video = cv2.VideoCapture(video_path)
    i = 1
    avg_blur = get_avg_blur(video_path)

    while True:
        success, frame = video.read()
        
        time_ms = video.get(cv2.CAP_PROP_POS_MSEC)
        
        if not success:
            print(f'decode_video_general: Failed to retrieve frame from video at {time_ms/1000} seconds.')
            break
        if is_blurry(frame, avg_blur): # video.read() when called iterates its own pointer, so continue works here
            continue

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
    avg_blur = get_avg_blur(video_path)

    skip_amount = float(end_pos - start_pos) / 50 # i want about 50 frames, takes about 4-8 minutes for model to process on my laptop
    time_ms = video.get(cv2.CAP_PROP_POS_MSEC)

    while True:
        success, frame = video.read()

        if not success:
            print(f'decode_video_specfic: Failed to retrieve frame from video at {time_ms/1000} seconds. (Or last frame was met)')
            break
        elif time_ms >= end_pos:
            break
        elif is_blurry(frame, avg_blur): 
            continue
        
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

def get_avg_blur(video_path: str):
    video = cv2.VideoCapture(video_path)
    blur_vars = []

    while True:
        success, frame = video.read()
        
        if not success:
            print("get_avg_blur failed or finished")
            break
        
        # convert to grayscale. laplacian, used for finding blurryness, doesn't work with color
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        laplacian_matrix = cv2.Laplacian(frame, cv2.CV_64F)
        blur_vars.append(laplacian_matrix.var())

    video.release()
    return statistics.mean(blur_vars)

def is_blurry(frame, avg_blur:float):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_matrix = cv2.Laplacian(frame, cv2.CV_64F)
    if laplacian_matrix.var() < avg_blur:
        return True
    return False
