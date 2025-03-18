import json
import csv
import pandas as pd
from datetime import datetime, timedelta
import random

def round_to_nearest_hour(t):
    dt = datetime.strptime(t, "%d/%m/%Y %H:%M")
    rounded_dt = dt + timedelta(minutes=30)
    return rounded_dt.replace(minute=0, second=0, microsecond=0)

def format_time(t):
    return f"{int(t)//100:02}:{int(t)%100:02}"

def get_random_range():
    # Random range between -21 to -4 hours and +4 to +23 hours
    start_range = random.randint(-21, -4)
    end_range = random.randint(4, 23)
    return start_range, end_range

# Load VIIRS data and JSON data
viirs_data = pd.read_csv(r'E:\\python_ground\Modis\\DL_FIRE_J1V-C2_406680\\viirs.csv')
with open(r'E:\\python_ground\Modis\\DL_FIRE_J1V-C2_406680\\filtered_weather_data.json', 'r') as file:
    weather_data = json.load(file)

# Process VIIRS data to get fire event timestamps
viirs_data['formatted_time'] = viirs_data['acq_time'].apply(format_time)
viirs_data['rounded_time'] = viirs_data['acq_date'] + ' ' + viirs_data['formatted_time']
viirs_data['rounded_timestamp'] = viirs_data['rounded_time'].apply(lambda x: round_to_nearest_hour(x).timestamp())

# Create a mapping of viirs_point to fire event timestamp
fire_event_mapping = {}
for index, row in viirs_data.iterrows():
    key = f"viirs_point_{index+1}_{row['acq_date']}_{row['latitude']},{row['longitude']}"
    fire_event_mapping[key] = row['rounded_timestamp']
counter = 1
# Process each VIIRS point separately
for viirs_point, hourly_data in weather_data.items():
    fire_timestamp = fire_event_mapping.get(viirs_point, None)
    start_range, end_range = get_random_range()

    # Format filename to avoid errors
    formatted_viirs_point = viirs_point.replace('/', '-').replace(',', '_')
    

    # Open a CSV file for each VIIRS point
    with open(f'{formatted_viirs_point}_weather_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['viirs_point', 'dt', 'temperature', 'humidity', 'wind_speed', 'rain', 'clouds', 'weather_main', 'weather_description', 'fire']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print(counter)
        counter +=1 
        if fire_timestamp:
            # Convert ranges to timestamps
            start_timestamp = fire_timestamp + (start_range * 3600)
            end_timestamp = fire_timestamp + (end_range * 3600)

            for hour in hourly_data:
                dt = hour['dt']
                if start_timestamp <= dt <= end_timestamp:
                    fire = 1 if dt == fire_timestamp else 0

                    # Write row to CSV
                    writer.writerow({
                        'viirs_point': viirs_point, 'dt': dt, 'temperature': hour['temp'],
                        'humidity': hour['humidity'], 'wind_speed': hour['wind_speed'],
                        'rain': hour.get('rain', 0), 'clouds': hour['clouds'],
                        'weather_main': hour['weather_main'], 'weather_description': hour['weather_description'],
                        'fire': fire
                    })

# Ensure that 'viirs.csv' and 'filtered_weather_data.json' are in the same directory as this script.
