import streamlit as st
import json
from datetime import datetime, timedelta
from components.charts import (
    create_weather_chart,
    create_post_chart,
    create_news_chart,
)

# Helper to load JSON and filter past 7 days
def load_and_filter_data(filepath, key="fetched_at"):
    try:
        with open(filepath, "r") as f:
            all_data = json.load(f)
    except Exception as e:
        st.error(f"Error reading {filepath}: {e}")
        return []

    one_week_ago = datetime.now() - timedelta(days=7)
    return [item for item in all_data if datetime.fromisoformat(item[key]) >= one_week_ago]

# Streamlit UI
st.title("📊 Data Lake Dashboard")

st.sidebar.header("Choose Chart Options")

# Weather Section
st.subheader("🌦️ Weather Data")
weather_chart_type = st.sidebar.selectbox("Weather Chart Type", ["Line", "Bar", "Pie"])
weather_data = load_and_filter_data("data_lake/weather_data.json")
if weather_data:
    create_weather_chart(weather_data, weather_chart_type)
else:
    st.warning("No weather data available.")

# Posts Section
st.subheader("📝 Posts Data")
post_chart_type = st.sidebar.selectbox("Posts Chart Type", ["Bar", "Pie"], key="posts")
post_data = load_and_filter_data("data_lake/posts_data.json")
if post_data:
    create_post_chart(post_data, post_chart_type)
else:
    st.warning("No post data available.")

# News Section
st.subheader("🗞️ News Data")
news_chart_type = st.sidebar.selectbox("News Chart Type", ["Bar", "Pie"], key="news")
news_data = load_and_filter_data("data_lake/news_data.json")
if news_data:
    create_news_chart(news_data, news_chart_type)
else:
    st.warning("No news data available.")


