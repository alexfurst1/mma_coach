from backend.video.analyze_video import analyze_video
from backend.video.video_decoder import decode_video

video_path = r'C:\Users\alexf\Documents\CSC\mma_coach\backend\upload\test_videos\IMG_2424.mov'

frames = decode_video(video_path)
output = analyze_video(frames)
print(output)
