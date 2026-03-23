from backend.video import analyze
from backend.video import decode
from backend.video.pull_metadata import pull_metadata
from backend.upload import upload_results

# uploads/IMG_2424.mov

video_path = r'C:\Users\alexf\Documents\CSC\mma_coach\backend\upload\test_videos\IMG_2424.mov'
pull_metadata('uploads/IMG_2424.mov')

frames = decode.decode_video_general(video_path)
output = analyze.analyze_video_general(frames)

#frames = decode.decode_video_specific(video_path, 20000, 25000)
#output = analyze.analyze_video_specific(frames)
print(type(output))
print(output)
upload_results.upload_general('uploads/IMG_2424.mov',output)

#pull_metadata
