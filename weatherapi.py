import requests
import database
from datetime import datetime, timedelta
import json
from functools import lru_cache
import time

# Constants
WEATHER_API_KEY = "c1cf373dc6ac4493968133550232011"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
CACHE_DURATION = 300  # 5 minutes cache

class WeatherAPIError(Exception):
    pass

@lru_cache(maxsize=128)
def get_cached_timestamp(lat, lon):
    """Helper function to track when weather data was last fetched"""
    return time.time()

def should_refresh_cache(lat, lon):
    """Check if we should refresh the cached weather data"""
    last_fetch = get_cached_timestamp(lat, lon)
    return (time.time() - last_fetch) > CACHE_DURATION

@lru_cache(maxsize=128)
def fetch_weather_data(lat, lon):
    """
    Fetches weather data from the WeatherAPI for the given latitude and longitude.
    Includes caching to prevent excessive API calls.
    """
    try:
        # Check cache first
        if not should_refresh_cache(lat, lon):
            return fetch_weather_data.cache_info()[0]  # Return cached value

        params = {
            "key": WEATHER_API_KEY,
            "q": f"{lat},{lon}"
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Update cache timestamp
            get_cached_timestamp(lat, lon)
            return data['current']['temp_c']
        elif response.status_code == 401:
            raise WeatherAPIError("Invalid API key")
        elif response.status_code == 429:
            raise WeatherAPIError("API rate limit exceeded")
        else:
            raise WeatherAPIError(f"API request failed with status code {response.status_code}")
            
    except requests.exceptions.Timeout:
        raise WeatherAPIError("Weather API request timed out")
    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"Weather API request failed: {str(e)}")
    except (KeyError, ValueError) as e:
        raise WeatherAPIError(f"Invalid response from Weather API: {str(e)}")

def calculate_temperature_difference(api_temp, device_temp):
    """
    Calculates the difference between API temperature and device temperature.
    Returns absolute difference and handles invalid inputs.
    """
    try:
        api_temp = float(api_temp)
        device_temp = float(device_temp)
        return abs(api_temp - device_temp)
    except (ValueError, TypeError) as e:
        print(f"Error calculating temperature difference: {str(e)}")
        return None

def get_heatmap_data(device_id):
    """
    Gets heatmap data for a specific device, including error handling
    and data validation.
    """
    try:
        # Get device location
        location = database.get_device_location(device_id)
        if not location:
            print(f"No location data available for device {device_id}")
            return []

        try:
            lat, lon = map(float, location.split(','))
        except ValueError:
            print(f"Invalid location format for device {device_id}: {location}")
            return []

        # Get device temperature
        device_data = database.get_latest_sensor_data(device_id)
        if not device_data or None in device_data:
            print(f"No sensor data available for device {device_id}")
            return []
        
        device_temp, _, _ = device_data

        try:
            # Get weather API temperature
            api_temp = fetch_weather_data(lat, lon)
            if api_temp is None:
                print(f"No weather data available for device {device_id}")
                return []

            # Calculate temperature difference
            temp_diff = calculate_temperature_difference(device_temp, api_temp)
            if temp_diff is None:
                return []

            print(f"Heatmap data for device {device_id}:")
            print(f"Location: {lat}, {lon}")
            print(f"Device temp: {device_temp}°C")
            print(f"API temp: {api_temp}°C")
            print(f"Difference: {temp_diff}°C")

            return [[lat, lon, temp_diff]]

        except WeatherAPIError as e:
            print(f"Weather API error for device {device_id}: {str(e)}")
            return []

    except Exception as e:
        print(f"Error generating heatmap data for device {device_id}: {str(e)}")
        return []


