# testing / debug / experimenting script, no use in the actual project

import os

folder_path = r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\frames_specific'
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path,filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
print('frames_specific has been cleared (test.py)')