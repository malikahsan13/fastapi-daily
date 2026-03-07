from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()


class EmailSchema(BaseModel):
    recipient_email: str
    subject: str
    body: str
