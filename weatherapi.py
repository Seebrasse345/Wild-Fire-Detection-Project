import requests
import database
from datetime import datetime, timedelta  
import json

# Constants
WEATHER_API_KEY = "c1cf373dc6ac4493968133550232011"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

def fetch_weather_data(lat, lon):
    """
    Fetches weather data from the WeatherAPI for the given latitude and longitude.
    """
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{lat},{lon}"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()['current']['temp_c']
    else:
        return None



def calculate_temperature_difference(api_temp, device_temp):
    """
    Calculates the difference between API temperature and device temperature.
    """
    return abs(api_temp - device_temp)

def get_heatmap_data(device_id,duration_minutes=3):
    location = database.get_device_location(device_id)
    if not location:
        return []
    lat,lon = map(float, location.split(','))
    # Get the average device temperature
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=duration_minutes)
    device_data = database.get_device_sensor_data(device_id, start_time, end_time)
    device_temps = [temp for temp, _ in device_data]
    if not device_temps:
        return []
    avg_device_temp = sum(device_temps) / len(device_temps)

    # Get the current temperature from the WeatherAPI
    api_temp = fetch_weather_data(lat, lon)
    if api_temp is None:
        return []

    # Calculate the temperature difference
    temp_diff = calculate_temperature_difference(avg_device_temp, api_temp)

    # Format for Leaflet heatmap: [lat, lon, intensity]
    return [lat, lon, temp_diff]


