from flask import Flask, jsonify, render_template
from flask_cors import CORS
from mqtt_sensor_finder import SensorDataProcessor
import threading
import database
import paho
import weatherapi

app = Flask(__name__)
CORS(app) 
database.create_table()

# Create an instance of the SensorDataProcessor
sensor_processor = SensorDataProcessor()

# Function to start the MQTT client in a separate thread
def start_mqtt_client():
    sensor_processor.run_mqtt_client()

# Start the MQTT client thread when the Flask application starts
mqtt_thread = threading.Thread(target=start_mqtt_client)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.route('/')
def index():
    # Serve the webpage that will display sensor data
    return render_template('index.html')

@app.route('/data')
def data():
    # Use the get_data method from the sensor_processor to fetch the latest sensor data
    temperature, humidity = sensor_processor.get_data()
    print(f"Temperature: {temperature}, Humidity: {humidity}")  # Debugging statement
    if temperature is not None and humidity is not None:
        return jsonify({
            'temperature': temperature,
            'humidity': humidity
        })
    else:
        # In case the data is None, send a message indicating that data is not available
        return jsonify({'message': 'Sensor data not available yet'}), 503

@app.route('/device-data')
def device_data():
    all_devices_data = database.get_all_devices_data()
    print(f"All devices data: {all_devices_data}")  # Debugging statement
    for device in all_devices_data:
        latest_temp, latest_humidity, latest_battery_voltage = database.get_latest_sensor_data(device['sensor_name'])
        device.update({'temperature': latest_temp, 'humidity': latest_humidity, 'battery_voltage': latest_battery_voltage})
    return jsonify(all_devices_data)

@app.route('/all-heatmap-data')
def all_heatmap_data():
    all_devices_data = database.get_all_devices_data()
    heatmap_data = []

    for device_data in all_devices_data:
        device_id, location = device_data['sensor_name'], device_data['location']
        print(f"Processing heatmap data for device: {device_id}")  # Debugging statement
        
        device_heatmap_data = weatherapi.get_heatmap_data(device_id)
        heatmap_data.extend(device_heatmap_data)

    print(f"Final heatmap data: {heatmap_data}")  # Debugging statement
    return jsonify(heatmap_data)

if __name__ == '__main__':
    app.run(debug=False, port=3000)