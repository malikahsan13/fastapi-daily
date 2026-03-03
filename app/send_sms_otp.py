from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import random

app = FastAPI()

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

otp_storage = {}

class Phone(BaseModel):
    phone_number: str
    
class VerifyOTP(BaseModel):
    phone_number: str
    otp: str
    
def generate_otp():
    return str(random.randint(1000,9999))

def send_otp(phone_number, otp):
    message = f"Your OTP is:{otp}"
    client.message.create(to=phone_number, from_=TWILIO_PHONE_NUMBER, body=message)
    
@app.post("/send-otp/")
async def send_otp_route(phone: Phone):
    otp = generate_otp()
    otp_storage[phone.phone_number] = otp
    send_otp(phone.phone_number, otp)
    return {"detail":"OTP sent successfully"}

@app.post("/verify-otp/")
async def verify_otp_route(otp_data:VerifyOTP):
    stored_otp = otp_storage.get(otp_data.phone_number)
    if not stored_otp:
        raise HTTPException(status_code=400, detail="OTP not found")
    if stored_otp != otp_data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    #Clear OTP after successful verification (optional)
    del otp_storage[otp_data.phone_number]
    return {"detail":"OTP verified successfully"}