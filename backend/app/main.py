from fastapi import FastAPI
from app.db import db
from fastapi import Query
from app.weather import fetch_weather_data

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Climate Hazard API is working"}

from fastapi import HTTPException
from app.weather import fetch_weather_data, geocode_location

@app.get("/weather")
async def get_weather(
    location: str = Query(..., description="City or place name"),
    start: str = Query(...),
    end: str = Query(...)
):
    try:
        lat, lon = await geocode_location(location)
    except ValueError:
        raise HTTPException(status_code=404, detail="Location not found")

    df = await fetch_weather_data(lat, lon, start, end)
    return df.head().to_dict(orient="records")
