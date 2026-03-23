from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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
    print(file.filename)
    return {'message': "File received.", 'name': file.filename}