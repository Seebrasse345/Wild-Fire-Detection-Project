1.database.py
This script handles the interaction with the SQLite database. It provides functions to:

Connect to the database
Create the sensor_readings table
Update sensor data
Retrieve device sensor data within a specified time range
Get device location
Fetch all devices' data
Get the latest sensor data for a specific device

2. weatherapi.py
This script interacts with the WeatherAPI to fetch weather data for a given latitude and longitude. It also calculates the temperature difference between the API temperature and the device temperature. The script provides a function to get heatmap data for a specific device.
3. mqtt_sensor_finder.py
This script handles the MQTT communication with the sensors. It subscribes to the MQTT topic for uplink messages and processes the received data. The script decodes the temperature, humidity, and battery voltage from the payload and updates the database with the new sensor data.
4. app.py
This script is the main Flask application. It serves the webpage that displays the sensor data and provides API endpoints for retrieving sensor data, device data, and heatmap data. The script also starts the MQTT client in a separate thread when the Flask application starts.
5. model_initial.py
This script trains a Random Forest model using the VIIRS and NASA data stored in CSV files. It performs the following steps:

Loads and preprocesses the data
Splits the data into training and testing sets
Performs feature engineering
Defines the hyperparameter grid for tuning
Trains the Random Forest model using grid search cross-validation
Evaluates the model on the test set
Visualizes the hyperparameter tuning results

Usage

Set up the necessary environment variables and configurations in the scripts.
Run app.py to start the Flask application.
Access the webpage served by the Flask application to view the sensor data.
The MQTT client will automatically start and process incoming sensor data.
Run model_initial.py to train the Random Forest model using the VIIRS and NASA data.
Dependencies
The project requires the following dependencies:

Flask
Flask-CORS
pandas
scikit-learn
matplotlib
paho-mqtt
