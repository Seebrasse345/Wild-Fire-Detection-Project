# Fire Detection System

A real-time fire detection system that uses IoT sensors to monitor temperature and humidity levels across multiple locations. The system includes a web interface with an interactive map showing sensor locations and temperature anomalies, and a machine learning model for fire prediction.

## Features

- Real-time temperature and humidity monitoring
- MQTT integration with The Things Network (TTN)
- Interactive map interface with sensor locations
- Heat map visualization of temperature anomalies
- Battery voltage monitoring for sensors
- Automatic data persistence using SQLite
- Weather API integration for temperature comparison
- Responsive web interface with real-time updates
- Machine learning-based fire prediction model
- Data analysis and visualization tools

## System Components
- Detector code back contains all the necessary sensor/assembly information
- Pi nano zero w based however it should work with any Raspberry above those specs

### IoT Monitoring System
- Real-time sensor data collection via MQTT
- Web-based dashboard for monitoring
- Database integration for historical data analysis

### Data Analysis & Visualization
- Data cleaning and preprocessing tools
- Advanced visualization for environmental conditions
- Correlation analysis between weather variables and fire events

### Machine Learning Fire Prediction
- Random Forest classifier for fire event prediction
- Weather data integration for enhanced prediction accuracy
- Model evaluation and performance metrics

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

## Data Processing and Model Training

### Data Cleaning

The system includes robust data cleaning tools to prepare raw sensor data for analysis and model training:

1. Run the data cleaner to process raw data files:
```bash
python data_cleaner.py
```

This script:
- Analyzes data quality issues
- Creates backups before modifying data
- Removes empty files
- Handles missing values using configurable strategies
- Provides detailed logging of all operations

### Data Visualization

Visualize patterns and insights from the collected data:

```bash
python data_visualization.py
```

The visualization module creates:
- Fire event distribution by day of the week
- Fire event distribution by hour of the day
- Correlation analysis between weather variables and fire events
- Fire probability analysis by temperature and humidity

All visualizations are saved to a timestamped directory for easy tracking and comparison.

### Model Training

Train the machine learning model for fire prediction:

```bash
python model_initial.py
```

The model training pipeline:
1. Loads and preprocesses data from the features directory
2. Performs feature engineering
3. Conducts hyperparameter tuning using grid search
4. Evaluates model performance with comprehensive metrics
5. Generates visualizations of model performance
6. Saves the trained model for later use

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

6. **Data Processing (`data_cleaner.py`)**
   - Cleans and prepares sensor data
   - Handles missing values
   - Ensures data quality

7. **Data Visualization (`data_visualization.py`)**
   - Creates insightful visualizations
   - Analyzes fire patterns
   - Generates reports on fire events

8. **Machine Learning Model (`model_initial.py`)**
   - Trains Random Forest classifier
   - Evaluates model performance
   - Provides feature importance analysis

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

## Machine Learning Model

The system includes a Random Forest classifier trained on historical weather and fire data:

- **Features**: temperature, humidity, wind speed, rainfall, cloud cover, hour of day, day of week
- **Target**: fire event occurrence (binary classification)
- **Performance metrics**: accuracy, precision, recall, F1-score
- **Hyperparameter tuning**: Grid search with cross-validation
- **Model persistence**: Models are saved using joblib for later deployment

## Data Analysis Insights

Analysis of the fire event data reveals several key patterns:

- Fire events show strong correlation with temperature and humidity levels
- Certain times of day and days of the week exhibit higher fire event frequencies
- Weather patterns including wind speed and cloud cover show significant impact on fire probability
- The dataset contains approximately 3.71% fire events, making it an imbalanced classification problem

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

4. **Model training errors:**
   - Ensure data files exist in the correct location
   - Check for missing or corrupted data files
   - Verify required Python packages are installed

## Contributing

Contributions are welcome! Please feel free to submit pull requests.
