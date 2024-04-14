import json
import database
database.create_table()

sample_output = '''
{
  "identifiers": [
    {"device_ids": {"device_id": "eui-a8610a32303f7904"}},
    {"device_ids": {"device_id": "eui-a8610a32303f7904"}},
    {"device_ids": {"device_id": "eui-a8610a32303f7904"}},
    {"device_ids": {"device_id": "eui-a8610a32303f7904"}},
    {"device_ids": {"device_id": "eui-a8610a32303f7904"}},
    {"device_ids": {"device_id": "eui-test"}}
  ]
}
'''

# Parse the JSON string
data = json.loads(sample_output)

# Extract device IDs
device_ids = [identifier["device_ids"]["device_id"] for identifier in data["identifiers"]]

# Populate the database
for device_id in device_ids:
    database.update_sensor_data(device_id, 17, 40)

print("Database populated with sample data.")
