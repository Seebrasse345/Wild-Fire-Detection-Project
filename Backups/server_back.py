import http.server
import socketserver
import threading
import webbrowser
import subprocess
import json
import base64
import paho.mqtt.client as mqtt

# TTN credentials
username = "fired1@ttn"
password = "NNSXS.J6MUXDXV6FYROTE2SNZY73FBXNMFNTS6DI6IBDY.CSZSDJQ6RRXHLYB6NB7REB4VAW2U25JGNFZVDTUHFJXPZAKSAMKA"

# Rest of your code...


# Path to the HTML file
html_file_path = "map.html"

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

processor = SensorDataProcessor()
mqtt_broker = "eu1.cloud.thethings.network"  # replace with your region's MQTT broker
mqtt_port = 1883
mqtt_topic = "#"

def mqtt_thread():
    client = mqtt.Client()
    client.on_connect = processor.on_connect
    client.on_message = processor.on_message

    client.username_pw_set(username, password)
    client.connect(mqtt_broker, mqtt_port, 60)

    client.loop_forever()

def open_browser():
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    # Start the MQTT thread
    mqtt_thread = threading.Thread(target=mqtt_thread)
    mqtt_thread.start()

    # Start the simple HTTP server in a separate thread
    server_thread = threading.Thread(target=lambda: subprocess.run(['python', '-m', 'http.server', '8000']))
    server_thread.start()

    # Open the web browser after a short delay to allow the server to start
    threading.Timer(2, open_browser).start()
