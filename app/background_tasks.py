from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import smtplib
from email.mime.text import MIMEText

app = FastAPI()


class EmailSchema(BaseModel):
    recipient: str
    subject: str
    body: str
