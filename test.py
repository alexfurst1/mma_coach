# testing / debug / experimenting script, no use in the actual project

import os
import shutil

folder_path = r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\frames_general'
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)          # delete loose files
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)      # delete subfolders and everything inside
print('frames_general has been cleared (test.py)')

if os.path.isfile(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4'):
        os.remove(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4')
print("video removed (test.py)")