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


@app.get("/read-csv/")
async def read_csv(file_name: str):
    try:
        with open(file_name, "r") as f:
            csv_reader = csv.DictReader(f)
            json_data = [row for row in csv_reader]
            return json_data

    except FileNotFoundError:
        return {"error": "File not found"}


@app.post("/write-csv/")
async def write_csv(data: CSVRequest):
    with open(data.filename, "a", newline="") as f:
        fieldnames = ['id', 'name', 'email']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # check if the file is empty
        if f.tell() == 0:
            writer.writeheader()

        for item in data.data:
            writer.writerow(item.dict())

    return {"message": "JSON data appended to CSV file successfully."}
