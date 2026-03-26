from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.upload.upload import upload_video
import av
import io
from fastapi import HTTPException, status
from backend.upload import upload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
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
    container.close()
    metadata = upload.access_metadata(container)
    upload_video(contents, filename, metadata)

