import threading
from mqtt_sensor_finder import SensorDataProcessor
import time
import database

def run():
    processor = SensorDataProcessor()
    thread = threading.Thread(target=processor.run_mqtt_client)
    thread.start()

    try:
        while True:
            time.sleep(5)  # Adjust the sleep time as needed
            with processor.lock:
                for device_eui, data in processor.device_data.items():
                    if data["temp"] is not None and data["hum"] is not None and data["battery_voltage"] is not None:
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        print(f"Device EUI: {device_eui}")
                        print(f"Temperature: {data['temp']} °C")
                        print(f"Humidity: {data['hum']} %")
                        print(f"Battery Voltage: {data['battery_voltage']} V")
                        print(f"Timestamp: {timestamp}")
                        print("---")

                        # Update the database with the latest sensor data
                        database.update_sensor_data(device_eui, data["temp"], data["hum"], data["battery_voltage"])

    except KeyboardInterrupt:
        print("Stopping the display script...")

if __name__ == "__main__":
    # Create the database table if it doesn't exist
    database.create_table()
    run()
