import pandas as pd
import httpx

BASE_URL = "https://archive-api.open-meteo.com/v1/era5"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

async def geocode_location(location_name: str) -> tuple[float, float]:
    """
    Fetch latitude and longitude for a given location name using Open-Meteo's Geocoding API.
    Returns (latitude, longitude).
    Raises ValueError if location is not found.
    """
    params = {"name": location_name, "count": 1, "format": "json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(GEOCODE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    results = data.get("results")
    if not results:
        raise ValueError(f"Location '{location_name}' not found.")

    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    return latitude, longitude


async def fetch_weather_data(latitude: float, longitude: float, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical daily maximum temperature data for a location and date range.
    Returns a cleaned Pandas DataFrame with 'date' and 'temp_max'.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max",
        "timezone": "UTC"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    # Extract data
    dates = data["daily"]["time"]
    temps = data["daily"]["temperature_2m_max"]

    # Create DataFrame
    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "temp_max": temps
    }).dropna()

    return df
