from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.upload.upload import upload_video
import av
import io
from fastapi import HTTPException, status
from backend.upload import upload
from backend.storage.supabase_client import supabase_client
from backend.storage import cloudflare_client 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    contents = await file.read()
    file_stream = io.BytesIO(contents)
    try:
        container = av.open(file_stream)
    
        if len(container.streams.video) == 0: # checks if file is a video type. will always be > 0 if its a video
            container.close() 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file contains no video tracks."
            )
        
    except (av.InvalidDataError, av.FormatError):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File format not recognized as a valid video container."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error processing video metadata."
        )
    metadata = upload.access_metadata(container)
    upload_video(contents, filename, metadata)
    container.close()

@app.get('/api/videos')
def get_videos():
    try:
        response = supabase_client.table('video_data').select('*').execute()
    except Exception as e:
        print(f'Error fetching from supabase: {e}')
    return response.data

@app.get('/api/videos/{video.id}/url')
def get_video_url(video_id: str):
    response = supabase_client.table('video_data').select('cloudflare_key').eq('id',video_id).execute()
    cloudflare_key = response.data['cloudflare_key']

    url = cloudflare_client.s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket':cloudflare_client.bucket_name,
            'Key':cloudflare_key
        },
        ExpiresIn=3600
    )

    return {'url':url}