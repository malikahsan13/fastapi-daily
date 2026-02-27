from fastapi import FastAPI, Response, Request, Cookie

app = FastAPI()

@app.get("/set_cookie/")
async def set_cookie(response: Response):
    response.set_cookie(key="cookie_key", value="cookie_value")
    return {"message":"Cookie value set successfully"}

@app.get("/get_cookie/")
async def get_cookie(request: Request):
    cookie_value = request.get("cookie_key")
    return {"Cookie value": cookie_value}