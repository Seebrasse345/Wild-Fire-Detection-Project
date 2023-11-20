import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('sensor_data.db')

def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (
                            sensor_name TEXT PRIMARY KEY,
                            location TEXT,
                            temperatures TEXT,
                            humidities TEXT,
                            timestamps TEXT)''')
        conn.commit()

def update_sensor_data(sensor_name, temperature, humidity):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT temperatures, humidities, timestamps, location FROM sensor_readings WHERE sensor_name = ?', (sensor_name,))
        row = cursor.fetchone()

        if row:
            # Append to existing data
            new_temperatures = f"{row[0]},{temperature}"  # Index 0 for temperatures
            new_humidities = f"{row[1]},{humidity}"  # Index 1 for humidities
            new_timestamps = f"{row[2]},{current_time}"  # Index 2 for timestamps
            location = row[3]  # Index 3 for location
        else:
            # Create new data strings
            new_temperatures = str(temperature)
            new_humidities = str(humidity)
            new_timestamps = current_time

            # Ask the user for location input
            location = input(f"Enter location for sensor {sensor_name}: ")
            if not location:
                location = "Unknown"  # Default location if user doesn't provide one

        # Insert or update the record
        cursor.execute('''INSERT OR REPLACE INTO sensor_readings 
                          (sensor_name, location, temperatures, humidities, timestamps)
                          VALUES (?, ?, ?, ?, ?)''', 
                          (sensor_name, location, new_temperatures, new_humidities, new_timestamps))
        conn.commit()
def get_device_sensor_data(device_id, start_time, end_time):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT temperatures, humidities, timestamps FROM sensor_readings WHERE sensor_name = ?', (device_id,))
        row = cursor.fetchone()
        if row:
            temperatures = row[0].split(',')
            humidities = row[1].split(',')
            timestamps = row[2].split(',')
            sensor_data = [(float(temp), float(hum)) for temp, hum, timestamp in zip(temperatures, humidities, timestamps)
                           if start_time <= datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') <= end_time]
            return sensor_data
        else:
            return []

def get_device_location(device_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT location FROM sensor_readings WHERE sensor_name = ?', (device_id,))
        row = cursor.fetchone()
        if row:
            return row[0]  # Assuming location is stored as "lat,lon"
        return None
def get_all_devices_data():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT sensor_name, location FROM sensor_readings')
        rows = cursor.fetchall()
        return [{'sensor_name': row[0], 'location': row[1]} for row in rows]
def get_latest_sensor_data(device_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT temperatures, humidities FROM sensor_readings WHERE sensor_name = ?', (device_id,))
        row = cursor.fetchone()
        if row:
            temperatures = row[0].split(',')
            humidities = row[1].split(',')
            return temperatures[-1], humidities[-1]  # Return the latest readings
        return None, None
