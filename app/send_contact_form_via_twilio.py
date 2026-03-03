from fastapi import FastAPI, Form, HTTPException
from twilio.rest import Client

app = FastAPI()

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""
RECIPIENT_WHATSAPP_NUMBER = ""
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

