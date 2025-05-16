import requests
import json
import os
from datetime import datetime

API_KEY = "916707eb4b0b4fda9e38b83693bf562f"
URL = f"https://newsapi.org/v2/everything?q=india&language=en&apiKey={API_KEY}"


response = requests.get(URL)
news_data = response.json().get("articles", [])

# Ensure each article has a 'publishedAt' field and add 'fetched_at'
cleaned_articles = []
for article in news_data:
    if not article.get("publishedAt"):
        continue  # Skip if no published date

    article["fetched_at"] = datetime.now().isoformat()
    cleaned_articles.append(article)

# File path
file_path = "data_lake/news_data.json"

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

# Append new valid articles
existing_data.extend(cleaned_articles)

# Save updated data
os.makedirs("data_lake", exist_ok=True)
with open(file_path, "w") as f:
    json.dump(existing_data, f, indent=4)
