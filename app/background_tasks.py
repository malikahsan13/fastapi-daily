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


def send_email(email: EmailSchema):
    # SMTP server configuration (change these values to your own)
    smpt_server = "smpt.gmail.com"
    smtp_port = 587
    smtp_username = "abc@gmail.com"
    smtp_password = "21123123"

    # Create a MIMEText object to represnt the email
    msg = MIMEText(email.body)
    msg['Subject'] = email.subject
    msg['From'] = smtp_username
    msg['To'] = email.recipient

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smpt_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, [email.recipient], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.post("/send-emails/")
async def send_email(emails: List[EmailSchema], background_tasks: BackgroundTasks):
    # Add send_email task to the background queue for each email
    for email in emails:
        background_tasks.add_task(send_email, email)
    return {"message": "Emails will be sent in the background"}
