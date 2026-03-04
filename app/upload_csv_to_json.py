from fastapi import FastAPI, UploadFile, File
import csv
import io

app = FastAPI()


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    if file.filename.endswith(".csv"):
        contents = await file.read()

        csv_data = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(csv_data)
        json_data = [row for row in csv_reader]
        return json_data
    else:
        return {"error": "Only CSV files are allowed"}
