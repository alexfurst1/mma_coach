from storage.cloudflare_client import s3, bucket_name
from storage.supabase_client import supabase
from boto3.s3.transfer import TransferConfig
import subprocess, json
import os

transfer_config = TransferConfig(
    multipart_threshold=1024 * 25, # 25MB threshold for multipart
    max_concurrency=10,            # Number of threads
    use_threads=True
)

def get_video_metadata(file_path):
    cmd = [
        'ffprobe', #using ffprobe is extremely fast because it doesn't render the video, it only reads the header. requires ffmpeg
        '-v', 'quiet', #reduces the lengthy chat that ffprobe usually produces
        '-print_format', 'json', # formats output as json
        '-show_format',  # gets info about the 'box' of the video (res,extension,size,length)
        '-show_steams', #shows video and audio streams
        file_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    data = json.loads(result.stdout)

    duration = float(data['format']['duration'])
    file_type = data['format']['format_name']

    return duration, file_type

def upload_video(file_path,video_type):
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
        print(f"Error: {e}")

    try: