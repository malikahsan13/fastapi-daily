from fastapi import FastAPI, UploadFile, File
import io
import csv
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()


class CSVData(BaseModel):
    name: str
    email: str
    id: int


class CSVRequest(BaseModel):
    data: List(CSVData)
    filename: str


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if file.filename.endswith(".csv"):
        contents = await file.read()

        with open(file.filename, wb) as f:
            f.write(contents)

        return {"message": "CSV file uploaded successfully"}
    else:
        return {"error": "Only CSV file are allowed"}
