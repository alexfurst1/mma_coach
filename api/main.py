from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import av, io, os
from fastapi import HTTPException, status
from backend.upload import upload, upload_results
from backend.storage.supabase_client import supabase_client
from backend.storage import cloudflare_client 
from backend.video import decode, analyze
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post('/upload')
async def upload_file(fightType:str = Form(...),sport:str = Form(...), file: UploadFile = File(...)):
    filename = file.filename
    contents = await file.read() # loads file into memory as bytes
    file_stream = io.BytesIO(contents) # wraps bytes in a stream
    
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
    metadata = upload.access_metadata(container,fightType,sport)
    await file.seek(0)
    await upload.upload_video(file, filename, metadata)
    container.close()

@app.get('/api/videos')
def get_videos():
    try:
        response = supabase_client.table('video_data').select('*').execute()
    except Exception as e:
        print(f'Error fetching from supabase: {e}')
    return response.data

@app.get('/api/videos/{video_id}/url')
def get_video_url(video_id: str):
    try:
        response = supabase_client.table('video_data').select('cloudflare_key').eq('id',video_id).execute()
        cloudflare_key = response.data[0]['cloudflare_key']
    except Exception as e:
        print(f'Error fetching cloudflare video. Error: {e}')
    url = cloudflare_client.s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket':cloudflare_client.bucket_name,
            'Key':cloudflare_key
        },
        ExpiresIn=3600
    )

    return {'url':url}

@app.post('/api/analyzeGeneral')
def analyzeGeneral(data: dict):
    video_id = data['video_id']
    cloudflare_key = data['video_cfkey']
    fight_type = str(data['fight_type'])
    sport = str(data['sport'])
    
    # download cloudflare video

    url = cloudflare_client.s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket':cloudflare_client.bucket_name,
            'Key':cloudflare_key
        },
        ExpiresIn=3600
    )

    try:
        response=requests.get(url)
    except Exception as e:
        print(f'Error: {response.status_code},{e}')

    with open(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4','wb') as f:
        f.write(response.content)
    
    # upload pipeline
    
    frames_filepaths = decode.decode_video_general(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4')
    analyzation = analyze.analyze_video_general(frames_filepaths,sport,fight_type)
    upload_results.upload_general(video_id,analyzation)
    print("Video analyzed, and feedback pushed to supabase.")

    # clear frames folder for next analyzation

    folder_path = r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\frames_general'
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path,filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
    print('frames_general has been cleared')

    # delete video 

    if os.path.isfile(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4'):
        os.remove(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4')
        print("video removed")

@app.post('/api/analyzeLocal')
def analyzeLocal(data: dict):
    video_id = data['video_id']
    cloudflare_key = data['video_cfkey']
    startPos = float(data['startPos'])
    endPos = float(data['endPos'])
    sport = str(data['sport'])
    fight_type = str(data['fight_type'])

    url = cloudflare_client.s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket':cloudflare_client.bucket_name,
            'Key':cloudflare_key
        },
        ExpiresIn=3600
    )

    try:
        response=requests.get(url)
    except Exception as e:
        print(f'Error: {response.status_code},{e}')

    with open(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4','wb') as f:
        f.write(response.content)

    frames_filepaths = decode.decode_video_specific(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4', startPos, endPos)
    analysis = analyze.analyze_video_specific(frames_filepaths,sport,fight_type)
    upload_results.upload_specific(video_id, analysis, startPos, endPos)
    print("timestamp analyzation completed and uploaded to supabase.")

    # clear frames folder, delete analyzed video from local directory.

    folder_path = r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\frames_specific'
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path,filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
    print('frames_specific has been cleared')

    # delete video 

    if os.path.isfile(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4'):
        os.remove(r'C:\Users\alexf\Documents\CSC\mma_coach\backend\video\saved_videos\video.mp4')
        print("video removed")
    
@app.get('/getAnalysisGeneral/{video_id}')
def get_general(video_id):
    try:
        response = supabase_client.table('summaries').select('*').eq('video_id',video_id).execute()
        data = response.data
        return data
    except Exception as e:
        print(f'Error: {e}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getAnalysisLocal/{video_id}')    
def get_local(video_id):
    try:
        response = supabase_client.table('timestamps').select('*').eq('video_id',video_id).execute()
        data = response.data
        return data
    except Exception as e: 
        print(f'Error: {e}')
        raise HTTPException(status_code=500, detail=str(e))
    
