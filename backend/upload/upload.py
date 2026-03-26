import av
import io
from backend.storage.cloudflare_client import s3_client
from backend.storage import cloudflare_client

def upload_video(file, filename, metadata):
    file_obj = io.BytesIO(file) # wrap bytes in a stream

    try:
        s3_client.upload_fileobj(
            file_obj,
            cloudflare_client.bucket_name,
            filename,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
    except Exception as e:
        print(f'Error with uploading video: {e}')

def access_metadata(container):
    video_stream = container.streams.video[0]

    metadata = {
        'file_type':None,
        'duration':float(container.duration / 1000000),
        'fps':float(video_stream.average_rate),
        'codec':video_stream.codec_context.name # just in case codec is needed
    }

    container.close()
    return metadata