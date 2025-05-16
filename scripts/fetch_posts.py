import requests
import json
import os
from datetime import datetime

# API Endpoint for posts
URL = "https://jsonplaceholder.typicode.com/posts"

# Fetch data
response = requests.get(URL)
posts_data = response.json()

# Add timestamp to each post
timestamp = datetime.now().isoformat()
for post in posts_data:
    post["fetched_at"] = timestamp

# Ensure data_lake folder exists
os.makedirs("data_lake", exist_ok=True)

# File path
file_path = "data_lake/posts_data.json"

# Load existing data
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
existing_data.extend(posts_data)

# Save updated data
with open(file_path, "w") as f:
    json.dump(existing_data, f, indent=4)
