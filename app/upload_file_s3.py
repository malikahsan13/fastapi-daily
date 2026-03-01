from fastapi import FastAPI, UploadFile, File
import boto3

app = FastAPI()

AWS_ACCESS_KEY_ID =
AWS_SECRET_ACCESS_KEY =
AWS_REGEION_NAME =
S3_BUCKET_NAME =


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGEION_NAME
        )

        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            file.filename
        )

        image_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGEION_NAME}.amazonaws.com/{file.filename}"

        return {"url": image_url}
    except Exception as e:
        return {"error": str(e)}
