from fastapi import FastAPI, File, UploadFile
import cloudinary
from cloudinary.uploader import upload

app = FastAPI()

cloudinary.config(
    cloud_name="",
    api_key="",
    api_secret=""
)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        result = upload(file.file)
        return {"url": result['secure_url']}
    except Exception as e:
        return {"error": str(e)}
