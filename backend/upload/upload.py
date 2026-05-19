import io
from backend.storage.cloudflare_client import s3_client
from backend.storage import cloudflare_client
from backend.storage.supabase_client import supabase_client

def upload_video(file, filename, metadata):
    file_obj = io.BytesIO(file) # wrap bytes in a stream

    try:
        response = s3_client.upload_fileobj(
            file_obj,
            cloudflare_client.bucket_name,
            filename,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code == 200:
            print('Video uploaded to cloudflare successfully. HTTP 200 OK')
        else:
            print(f'Error uploading video to cloudflare. {status_code} ')
    except Exception as e:
        print(f'Error with uploading video to cloudflare: {e}')

    try:
        response = supabase_client.table('video_data').insert({
            'cloudflare_key':f'uploads/{filename}',
            'duration':metadata['duration'],
            'video_type':'muay thai'
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