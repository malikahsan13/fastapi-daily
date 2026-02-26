from fastapi import FastAPI, Form


app = FastAPI()


@app.post("/submit_form/")
async def submit_form(username: str = Form(...), password: str = Form(...)):
    print("username", username)
    print("password", password)
    return {"message": "form submitted successfully", "username": username}
