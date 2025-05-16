import requests
import json
import os
from datetime import datetime

API_KEY = "08c471681599404c70716eb064822af0"
CITY = "Chennai"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

# Add timestamp
data["fetched_at"] = datetime.now().isoformat()

# File path
file_path = "data_lake/weather_data.json"

# Load existing data or create a new list
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        try:
            existing_data = json.load(f)
            if isinstance(existing_data, dict):
                existing_data = [existing_data]
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

# Append new data
existing_data.append(data)

# Save back to file
with open(file_path, "w") as f:
    json.dump(existing_data, f, indent=4)
