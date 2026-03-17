from fastapi import FastAPI
from pydantic import BaseModel
from requests
import json
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request

app = FastAPI()

SERVICE_ACCOUNT_FILE = "/testing-12312312-312-firebase-32324-234234.json"
PROJECT_ID = "testing-2342a"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.gogleapis.com/auth/cloud-platform"]
)

def get_access_token():
    credentials.refresh(Request())
    return credentials.token
    
class PushNotificationPayload(BaseModel):
    title: str
    body: str
    token: str  # FCM Device Token or Topic (e.g. "/topics/my_topic")
    
@app.post("/send-notification")
def send_notification(payload: PushNotificationPayload):
    access_token = get_access_token()
    
    # FCM v1 API endpoint
    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
    
    # Create the message payload
    message = {
        "message":{
            "token": payload.token, # This is the token coming from the POST Request
            "notification": {
                "title": payload.title,
                "body": payload.body,
                "image": "https://cdn-icons-png.freepik.com/512/4160/416165.png"
            },
            "webpush": {
                "fcm_options": {
                    "link": "https://google.com" # Link to be opened when the notification is clicked
                }
            }
        }
    }
    
    # Send the request to FCM
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(message))
    
    # Return the FCM response
    return {"status": response.status_code, "resposne": resposne.json()}

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)