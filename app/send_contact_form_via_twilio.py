from fastapi import FastAPI, Form, HTTPException
from twilio.rest import Client

app = FastAPI()

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""
RECIPIENT_WHATSAPP_NUMBER = ""
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/send-whatsapp/")
async def send_whatsapp(name: str= Form(...), email: str = Form(...), message: str = Form(...)):
    try:
        whatsapp_msg = f"New contact form submission:\nName: {name}\nEmail: {email}\nMessage:{message}"
        message = client.message.create(
            body=whatsapp_msg,
            form_= "whatsapp:"+TWILIO_PHONE_NUMBER,
            to="whatsapp:"+RECIPIENT_WHATSAPP_NUMBER
        )
        return {"status":"success","message_sid":message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))