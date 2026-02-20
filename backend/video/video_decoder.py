# video_decoder.py - decodes video into frames that can be understood by vision model
import cv2

def decode_video(video_path:str):
    frames = []

    video = cv2.VideoCapture(video_path)

    while True:
        success, frame = video.read()
        time_ms = video.get(cv2.CAP_PROP_POS_MSEC)
        
        if not success:
            print(f'Failed to retrieve frame from video at {time_ms/1000} seconds.')
            break
        frames.append(frame)
        video.set(cv2.CAP_PROP_POS_MSEC, (3000 + time_ms))

    video.release()

    return frames