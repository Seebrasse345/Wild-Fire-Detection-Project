import threading
from mqtt_sensor_finder import SensorDataProcessor
import time
def run():
    processor = SensorDataProcessor()
    thread = threading.Thread(target=processor.run_mqtt_client)
    thread.start()

    try:
        while True:
            # Update this interval as needed
            time.sleep(5)  # Adjust the sleep time as needed
            with processor.lock:
                if processor.battery_voltage is not None:
                    print(f"Latest Battery Voltage: {processor.battery_voltage} V")
    except KeyboardInterrupt:
        print("Stopping the display script...")

if __name__ == "__main__":
    run()
