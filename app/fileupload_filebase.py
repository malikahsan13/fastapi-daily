# Project name on firebase = fastapi-test-33eac
from fastapi import FastAPI, UploadFile, File, HTTPException
from firebase_admin import credentials, storage, initialize_app
from typing import Optional


app = FastAPI()

cred = credentials.Certificate("./xxx.json")
firebase_app = initialize_app(cred, {"storageBucket": "bucket-name-here"})


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), path: Optional[str] = None):
    if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Only image file allowed")

    if not path:
        path = file.filename

    bucket = storage.bucket()
    blob = bucket.blob(path)
    blob.upload_from_string(await file.read(), content_type=file.content_type)

    url = blob.generate_signed_url()
    return {"url": url}
