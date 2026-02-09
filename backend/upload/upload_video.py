from backend.storage.cloudflare_client import s3, bucket_name
from backend.storage.supabase_client import supabase
from boto3.s3.transfer import TransferConfig
import os
from pathlib import Path
import cv2

transfer_config = TransferConfig(
    multipart_threshold=1024 * 25, # 25MB threshold for multipart
    max_concurrency=10,            # Number of threads
    use_threads=True
)

def get_video_metadata(file_path):
    
    file_type = Path(file_path).suffix[1:]

    cap = cv2.VideoCapture(str(file_path))

    if not cap.isOpened():
        raise ValueError(f'Could not open video file: {file_path}')
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    duration = frame_count / fps if fps > 0 else 0

    cap.release()

    return duration, file_type

def upload_video(file_path,video_type: str):
    duration, file_type = get_video_metadata(file_path)
    try:
        video_name = os.path.basename(file_path)
        object_key = f"uploads/{video_name}"

        s3.upload_file(
            Filename = file_path,
            Bucket = bucket_name,
            Key = object_key,
            Config = transfer_config,
            ExtraArgs = {
                'ContentType': f'video/{file_type}'
            }
        )
        print(f"Successfully uploaded {video_name} to bucket.")
    except Exception as e:
        print(f"Error uploading to cloudflare: {e}")

    try:
        upsert = (
            supabase.table('video_data')
            .upsert({'cloudflare_key':object_key,'status':'new','video_type':video_type, 'duration':duration})
            .execute()
        )
        print(f'Successfully uploaded video metadata for {video_name}')
    except Exception as e:
        print(f'Error with supabase video_data upload: {e}')

video_path = r'C:\Users\alexf\Documents\CSC\mma_coach\backend\upload\test_videos\IMG_2424.mov'
upload_video(video_path,'fight')