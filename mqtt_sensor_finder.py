import paho.mqtt.client as mqtt
import json
import base64
import time
import threading
import database 
class SensorDataProcessor:
    def __init__(self):
        self.temp = None
        self.hum = None
<<<<<<< Updated upstream
=======
        self.battery_voltage = None  
        self.device_data = {} 
>>>>>>> Stashed changes
        self.lock = threading.Lock()  # To ensure thread safety
    def run_mqtt_client(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.username_pw_set(username, password)
        client.connect(mqtt_broker, mqtt_port, 60)

        # Start the network loop in a separate thread
        client.loop_start()

<<<<<<< Updated upstream
    def process_data(self, payload_json):
=======

        
    def process_data(self, payload_json, device_eui):
>>>>>>> Stashed changes
        # Make sure this is an uplink message
        if 'uplink_message' in payload_json:
            frm_payload_base64 = payload_json['uplink_message']['frm_payload']
            frm_payload_bytes = base64.b64decode(frm_payload_base64)
        
            # Decode temperature (2 bytes, big endian)
            temperature_raw = frm_payload_bytes[2:4]
            temperature = (temperature_raw[0] << 8 | temperature_raw[1]) / 10.0
        
            # Decode humidity (1 byte)
            humidity_raw = frm_payload_bytes[6]
            humidity = humidity_raw / 2.0
        
            device_id = payload_json["identifiers"][0]["device_ids"]["device_id"]

            with self.lock:
<<<<<<< Updated upstream
                self.temp = temperature
                self.hum = humidity
                print(f"temp: {self.temp} *C")
                print(f"humidity: {self.hum} %")
=======
                if device_eui not in self.device_data:
                    self.device_data[device_eui] = {}  # Initialize the device_data for the new device
>>>>>>> Stashed changes

                self.device_data[device_eui]["temp"] = temperature
                self.device_data[device_eui]["hum"] = humidity
                self.device_data[device_eui]["battery_voltage"] = battery_voltage

                print(f"Device EUI: {device_eui}")
                print(f"temp: {temperature} *C")
                print(f"humidity: {humidity} %")
                print(f"Battery Voltage: {battery_voltage} V")
                print(f"Processed data for device {device_eui}: Temperature: {temperature}, Humidity: {humidity}, Battery Voltage: {battery_voltage}")
                # Update the database with new sensor data
<<<<<<< Updated upstream
                database.update_sensor_data(device_id, self.temp, self.hum)

=======
                database.update_sensor_data(device_eui, temperature, humidity, battery_voltage)
>>>>>>> Stashed changes
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribe to the specific topic for uplink messages
        client.subscribe(mqtt_topic)

    def on_message(self, client, userdata, msg):
        try:
            payload_json = json.loads(msg.payload.decode('utf-8'))
<<<<<<< Updated upstream
            # Only process if it's an uplink message
            if 'uplink_message' in payload_json:
                self.process_data(payload_json)
=======
            print("Received payload:", payload_json)
            if 'end_device_ids' in payload_json and 'device_id' in payload_json['end_device_ids']:
                device_eui = payload_json['end_device_ids']['device_id']
                self.process_data(payload_json, device_eui)
>>>>>>> Stashed changes
        except Exception as e:
            print("Error decoding payload:", e)

    def get_data(self):
        with self.lock:
            return self.temp, self.hum



# TTN credentials
username = "fired1@ttn"  # Your TTN application ID
password = "NNSXS.J6MUXDXV6FYROTE2SNZY73FBXNMFNTS6DI6IBDY.CSZSDJQ6RRXHLYB6NB7REB4VAW2U25JGNFZVDTUHFJXPZAKSAMKA"  # Your TTN application access key

# MQTT parameters
mqtt_broker = "eu1.cloud.thethings.network"  # replace with your region's MQTT broker
mqtt_port = 1883
mqtt_topic = "v3/fired1@ttn/devices/+/up"  # The topic to subscribe to for uplink messages




