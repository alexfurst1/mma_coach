import io
from backend.storage.cloudflare_client import s3_client
from backend.storage import cloudflare_client
from backend.storage.supabase_client import supabase_client

async def upload_video(file, filename: str, metadata: dict):
    contents = await file.read()
    file_obj = io.BytesIO(contents) # wrap bytes in a stream
    filename = f"uploads/{filename}"

    try:
        response = s3_client.upload_fileobj(
            file_obj,
            cloudflare_client.bucket_name,
            filename,
            ExtraArgs={'ContentType': file.content_type or 'application/octet-stream'} # tells R2 to store the upload's MIME type as the file's content type, falling back to the generic application/octet-stream if the upload didn't include one.
        ) # need because when the browser later fetches the video, R2 reports the correct content type so it can be played correctly
    except Exception as e:
        print(f'Error with uploading video to cloudflare: {e}')

    try:
        response = supabase_client.table('video_data').insert({
            'cloudflare_key':f'{filename}',
            'duration':metadata['duration'],
            'sport':metadata['sport'],
            'fight_type':metadata["fight_type"]
        }).execute()

        if response.data:
            print('Supabase insert successful (video_data)')
        else:
            print('Error inserting metadata to supabase')
    except Exception as e:
        print(f'Error uploading metadata to supabase: {e}')

def access_metadata(container,fight_type,sport):
    video_stream = container.streams.video[0]

    metadata = {
        'file_type':None,
        'duration':float(container.duration / 1000000),
        'fps':float(video_stream.average_rate),
        'fight_type':fight_type,
        'sport':sport
    }
    

    container.close()
    return metadata