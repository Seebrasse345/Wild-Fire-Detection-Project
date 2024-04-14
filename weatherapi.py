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
    try:
        api_temp = float(api_temp)
        return abs(api_temp - device_temp)
    except (ValueError, TypeError):
        print("Error: Invalid temperature values")
        return None

def get_heatmap_data(device_id):
    location = database.get_device_location(device_id)
    if not location:
        print("Failed to get device location")
        return []
    lat, lon = map(float, location.split(','))

    # Get the last available data point
    device_data = database.get_latest_sensor_data(device_id)
    if not device_data:
        print("No sensor data available for device", device_id)
        return []
    device_temp, _, _ = device_data

    # Get the current temperature from the WeatherAPI
    api_temp = fetch_weather_data(lat,lon)
    if api_temp is None:
        print("Failed to fetch weather data")
        return []

    # Calculate the temperature difference
    temp_diff = calculate_temperature_difference(device_temp, api_temp)
    if temp_diff is None:
        print("Failed to calculate temperature difference for device", device_id)
        return []

    print("success")
    print(temp_diff)
    
    # Format for Leaflet heatmap: [[lat, lon, intensity]]
    print([[lat,lon,temp_diff]])
    print(f"Heatmap data for device {device_id}: {[lat, lon, temp_diff]}")  # Debugging statement
    return [[lat, lon, temp_diff]]


