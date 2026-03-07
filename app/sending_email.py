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


@app.post("/send_email/")
async def send_email(email_data: EmailSchema):
    sender_email = "abc@mail.com"
    sender_password = "abc123"
    recipient_email = "bcd@mail.com"
    subject = email_data.subject
    body = email_data.body

    smtp_server = smtplib.SMTP("smtp@gmail.com", 587)
    smtp_server.starttls()
