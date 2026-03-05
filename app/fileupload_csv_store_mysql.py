from fastapi import FastAPI, UploadFile, File, HTTPException
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnect://root:Admin123@localhost/mydb"

Base = declarative_base()


class Item(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,  index=True)
    name = Column(String)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()

    csv_data = contents.decode("utf-8").splitlines()
    csv_reader = csv.reader(csv_data)

    db = SessionLocal()
    for row in csv_reader:
        item = Item(name=row[0], email=row[1])
        db.add(item)
    db.commit()
    db.close()

    return {"message": "CSV file uploaded and data stored in MySql"}
