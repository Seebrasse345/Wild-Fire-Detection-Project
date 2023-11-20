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
        self.lock = threading.Lock()  # To ensure thread safety
    def run_mqtt_client(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.username_pw_set(username, password)
        client.connect(mqtt_broker, mqtt_port, 60)

        # Start the network loop in a separate thread
        client.loop_start()

    def process_data(self, payload_json):
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
                self.temp = temperature
                self.hum = humidity
                print(f"temp: {self.temp} *C")
                print(f"humidity: {self.hum} %")

                # Update the database with new sensor data
                database.update_sensor_data(device_id, self.temp, self.hum)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribe to the specific topic for uplink messages
        client.subscribe(mqtt_topic)

    def on_message(self, client, userdata, msg):
        try:
            payload_json = json.loads(msg.payload.decode('utf-8'))
            # Only process if it's an uplink message
            if 'uplink_message' in payload_json:
                self.process_data(payload_json)
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
mqtt_topic = "v3/fired1@ttn/devices/eui-a8610a32303f7904/up"  # The topic to subscribe to for uplink messages




