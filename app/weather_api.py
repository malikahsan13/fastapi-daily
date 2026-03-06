from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()

API_KEY = ""
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("weather_index.html", {"request": request})


@app.get("/weather")
async def get_weather(city: str, request: Request):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temparature": data["main"]["tmp"],
                "weather": data["weather"][0]["description"]
            }
            return templates.TemplateResponse("weathter.html", {"request": request, "weather_data": weather_data})
        else:
            raise HTTPException(
                status_code=response.status_code, detail="City not found")
