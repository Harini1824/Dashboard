import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

def weather_dashboard(city_filter=None):
    file_path = "data_lake/weather_data.json"
    if not os.path.exists(file_path):
        st.error("No weather data found. Please run fetch_weather.py first.")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    # Extract relevant data to a dataframe
    records = []
    for entry in data:
        main = entry.get("main", {})
        weather = entry.get("weather", [{}])[0]
        records.append({
            "city": entry.get("name", ""),
            "date": entry.get("fetched_at", ""),
            "temp": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "weather_main": weather.get("main"),
            "weather_desc": weather.get("description"),
            "pressure": main.get("pressure"),
            "wind_speed": entry.get("wind", {}).get("speed"),
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])

    # Filter by city if given
    if city_filter:
        df = df[df["city"].str.contains(city_filter, case=False, na=False)]

    if df.empty:
        st.warning("No weather data available for this city.")
        return

    st.subheader("☀️ Weather Data")
    st.write(df)

    metric = st.selectbox("Select metric to plot", ["temp", "feels_like", "humidity", "pressure", "wind_speed"], key="weather_metric")
    fig_type = st.selectbox("Select graph type", ["Line", "Bar", "Scatter"], key="weather_graph_type")

    if fig_type == "Line":
        fig = px.line(df, x="date", y=metric, title=f"{metric.capitalize()} over time")
    elif fig_type == "Bar":
        fig = px.bar(df, x="date", y=metric, title=f"{metric.capitalize()} over time")
    else:
        fig = px.scatter(df, x="date", y=metric, title=f"{metric.capitalize()} over time")

    st.plotly_chart(fig)

