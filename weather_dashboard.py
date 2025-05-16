import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px

# Load data from file
file_path = "data_lake/weather_data.json"

@st.cache_data
def load_data(path):
    with open(path, "r") as f:
        data = json.load(f)
    # Normalize nested JSON to flat table
    records = []
    for entry in data:
        main = entry.get("main", {})
        weather = entry.get("weather", [{}])[0]  # first weather condition
        record = {
            "city": entry.get("name", ""),
            "date": entry.get("fetched_at", ""),
            "temp": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "weather_main": weather.get("main"),
            "weather_desc": weather.get("description"),
            "pressure": main.get("pressure"),
            "wind_speed": entry.get("wind", {}).get("speed"),
        }
        records.append(record)
    df = pd.DataFrame(records)
    # Convert date string to datetime
    df["date"] = pd.to_datetime(df["date"])
    return df

st.title("Weather Data Dashboard")

try:
    df = load_data(file_path)
except FileNotFoundError:
    st.error("No weather data file found. Please fetch data first.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# Filter by city
cities = df["city"].unique()
selected_city = st.sidebar.selectbox("Select City", cities)

# Filter by date range
min_date, max_date = df["date"].min(), df["date"].max()
start_date = st.sidebar.date_input("Start Date", min_date.date())
end_date = st.sidebar.date_input("End Date", max_date.date())

# Filter data accordingly
filtered_df = df[
    (df["city"] == selected_city) &
    (df["date"] >= pd.Timestamp(start_date)) &
    (df["date"] <= pd.Timestamp(end_date))
]

if filtered_df.empty:
    st.warning("No data for selected filters.")
    st.stop()

st.write(f"### Weather data for {selected_city} from {start_date} to {end_date}")
st.dataframe(filtered_df)

# Choose metric to plot
metric = st.selectbox("Select metric to plot", ["temp", "feels_like", "humidity", "pressure", "wind_speed"])

# Choose graph type
graph_type = st.selectbox("Select graph type", ["Line", "Bar", "Scatter"])

# Plot the graph
fig = None
if graph_type == "Line":
    fig = px.line(filtered_df, x="date", y=metric, title=f"{metric.capitalize()} over time")
elif graph_type == "Bar":
    fig = px.bar(filtered_df, x="date", y=metric, title=f"{metric.capitalize()} over time")
elif graph_type == "Scatter":
    fig = px.scatter(filtered_df, x="date", y=metric, title=f"{metric.capitalize()} over time")

st.plotly_chart(fig)
