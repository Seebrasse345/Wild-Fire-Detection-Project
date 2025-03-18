# Fire Detection System

A real-time fire detection system that uses IoT sensors to monitor temperature and humidity levels across multiple locations. The system includes a web interface with an interactive map showing sensor locations and temperature anomalies.

## Features

- Real-time temperature and humidity monitoring
- MQTT integration with The Things Network (TTN)
- Interactive map interface with sensor locations
- Heat map visualization of temperature anomalies
- Battery voltage monitoring for sensors
- Automatic data persistence using SQLite
- Weather API integration for temperature comparison
- Responsive web interface with real-time updates

## Prerequisites

- Python 3.7+
- The Things Network (TTN) account and application
- WeatherAPI.com API key
- Internet connection for MQTT and weather data

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
   - Update the TTN credentials in `mqtt_sensor_finder.py`
   - Update the Weather API key in `weatherapi.py`

## Configuration

### MQTT Configuration
In `mqtt_sensor_finder.py`, update the following variables with your TTN credentials:
```python
username = "your-ttn-application-id"
password = "your-ttn-access-key"
mqtt_broker = "your-region.cloud.thethings.network"
```

### Weather API Configuration
In `weatherapi.py`, update the API key:
```python
WEATHER_API_KEY = "your-weather-api-key"
```

## Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Access the web interface at `http://localhost:3000`

## System Architecture

### Components:
1. **Flask Backend (`app.py`)**
   - Serves the web interface
   - Handles API endpoints for sensor data
   - Manages MQTT client connection

2. **MQTT Client (`mqtt_sensor_finder.py`)**
   - Connects to TTN
   - Processes incoming sensor data
   - Decodes payload data

3. **Database (`database.py`)**
   - SQLite database for data persistence
   - Stores sensor readings and locations
   - Manages historical data

4. **Weather Integration (`weatherapi.py`)**
   - Fetches current weather data
   - Calculates temperature anomalies
   - Provides data for heatmap visualization

5. **Web Interface (`templates/index.html`)**
   - Interactive map using Leaflet.js
   - Real-time sensor data display
   - Heatmap visualization

## API Endpoints

- `/` - Main web interface
- `/data` - Latest sensor readings
- `/device-data` - All device information and latest readings
- `/all-heatmap-data` - Temperature anomaly data for heatmap

## Sensor Data Format

The system expects sensor data in the following format:
- Temperature: 2 bytes, big-endian, scaled by 10
- Humidity: 1 byte, scaled by 2
- Battery voltage: Included in payload

## Troubleshooting

1. **No sensor data appearing:**
   - Check TTN credentials
   - Verify MQTT connection
   - Ensure sensors are transmitting

2. **Heatmap not showing:**
   - Verify Weather API key
   - Check sensor locations are properly set
   - Ensure temperature data is being received

3. **Database issues:**
   - Check file permissions for `sensor_data.db`
   - Verify table schema using SQLite browser

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

[Your chosen license]
