from fastapi import FastApi, HTTPException
from twilio.rest import Client

app = FastApi()

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.post("/send-sms/")
async def send_sms(to: str, body: str):
    try:
        message = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,
            body=body
        )
        return {"status": "success", "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
