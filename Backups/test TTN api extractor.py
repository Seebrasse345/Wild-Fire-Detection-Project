import paho.mqtt.client as mqtt
import json
import base64
import time
import threading

class SensorDataProcessor:
    def __init__(self):
        self.temp = None
        self.hum = None
        self.lock = threading.Lock()  # To ensure thread safety

    def process_data(self, payload_json):
        frm_payload_base64 = payload_json['uplink_message']['frm_payload']
        frm_payload_bytes = base64.b64decode(frm_payload_base64)
        hex_payload = frm_payload_bytes.hex()

        print(f"Decoded Hex Payload: {hex_payload}")
        hex_p = list(hex_payload)

        temp = hex_p[0:8]
        hum = hex_p[8:]
        for n in range(0, 4):
            temp.pop(0)
            hum.pop(0)

        temp.pop(0)
        temp.pop(0)
        hum = "".join(hum)
        temp = "".join(temp)

        with self.lock:
            self.temp = int(temp, 16) / 10
            self.hum = int(hum, 16)
            print(f"temp: {self.temp} *C")
            print(f"humidity: {self.hum} %")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(mqtt_topic)

    def on_message(self, client, userdata, msg):
        try:
            payload_json = json.loads(msg.payload.decode('utf-8'))
            self.process_data(payload_json)
        except Exception as e:
            print("Error decoding payload:", e)

    def get_data(self):
        with self.lock:
            return self.temp, self.hum

def mqtt_thread():
    client = mqtt.Client()
    client.on_connect = processor.on_connect
    client.on_message = processor.on_message

    client.username_pw_set(username, password)
    client.connect(mqtt_broker, mqtt_port, 60)

    client.loop_forever()

# TTN credentials
username = "fired1@ttn"
password = "NNSXS.J6MUXDXV6FYROTE2SNZY73FBXNMFNTS6DI6IBDY.CSZSDJQ6RRXHLYB6NB7REB4VAW2U25JGNFZVDTUHFJXPZAKSAMKA"

# MQTT parameters
mqtt_broker = "eu1.cloud.thethings.network"  # replace with your region's MQTT broker
mqtt_port = 1883
mqtt_topic = "#"

processor = SensorDataProcessor()

mqtt_thread = threading.Thread(target=mqtt_thread)
mqtt_thread.start()

# Access temp and hum variables continuously
while True:
    temp, hum = processor.get_data()
    print(f"Current temp: {temp} *C, Current humidity: {hum} %")
    # Add a delay to avoid excessive printing
    time.sleep(20) #Messages currently set to send every 30 seconds ish so 35 for safety
