from flask import Flask, jsonify, render_template
from flask_cors import CORS
from mqtt_sensor_finder import SensorDataProcessor
import threading
import database
import paho
import weatherapi
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Ensure database is initialized
try:
    database.create_table()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise

# Create an instance of the SensorDataProcessor
sensor_processor = SensorDataProcessor()

def start_mqtt_client():
    """Function to start the MQTT client in a separate thread"""
    try:
        sensor_processor.run_mqtt_client()
    except Exception as e:
        logger.error(f"MQTT client error: {str(e)}")
        # Attempt to reconnect after a delay
        threading.Timer(30.0, start_mqtt_client).start()

# Start the MQTT client thread
mqtt_thread = threading.Thread(target=start_mqtt_client)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.route('/')
def index():
    """Serve the main webpage"""
    return render_template('index.html')

@app.route('/data')
def data():
    """Get the latest sensor data"""
    try:
        temperature, humidity = sensor_processor.get_data()
        logger.debug(f"Retrieved sensor data - Temperature: {temperature}, Humidity: {humidity}")
        
        if temperature is not None and humidity is not None:
            return jsonify({
                'temperature': temperature,
                'humidity': humidity
            })
        else:
            return jsonify({'message': 'Sensor data not available yet'}), 503
    except Exception as e:
        logger.error(f"Error retrieving sensor data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/device-data')
def device_data():
    """Get data for all devices"""
    try:
        all_devices_data = database.get_all_devices_data()
        logger.debug(f"Retrieved data for {len(all_devices_data)} devices")
        
        for device in all_devices_data:
            latest_temp, latest_humidity, latest_battery_voltage = database.get_latest_sensor_data(device['sensor_name'])
            device.update({
                'temperature': latest_temp,
                'humidity': latest_humidity,
                'battery_voltage': latest_battery_voltage
            })
        return jsonify(all_devices_data)
    except Exception as e:
        logger.error(f"Error retrieving device data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/all-heatmap-data')
def all_heatmap_data():
    """Get heatmap data for all devices"""
    try:
        all_devices_data = database.get_all_devices_data()
        heatmap_data = []

        for device_data in all_devices_data:
            device_id = device_data['sensor_name']
            logger.debug(f"Processing heatmap data for device: {device_id}")
            
            try:
                device_heatmap_data = weatherapi.get_heatmap_data(device_id)
                heatmap_data.extend(device_heatmap_data)
            except Exception as e:
                logger.error(f"Error processing heatmap data for device {device_id}: {str(e)}")
                continue

        logger.debug(f"Generated heatmap data with {len(heatmap_data)} points")
        return jsonify(heatmap_data)
    except Exception as e:
        logger.error(f"Error generating heatmap data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 3000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask application on port {port} (debug={debug})")
    app.run(debug=debug, port=port)