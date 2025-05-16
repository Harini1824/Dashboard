import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import plotly.express as px

# Utility to load and clean JSON data
def load_data(filepath, date_key=None):
    if not os.path.exists(filepath):
        return pd.DataFrame()
    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
            df = pd.DataFrame(data)
            if date_key in df.columns:
                df[date_key] = pd.to_datetime(df[date_key], errors='coerce')
            return df
        except Exception:
            return pd.DataFrame()

# Load datasets
weather_df = load_data("data_lake/weather_data.json", "fetched_at")
news_df = load_data("data_lake/news_data.json", "fetched_at")
posts_df = load_data("data_lake/posts_data.json", "fetched_at")

st.title("📊 Unified Interactive Data Dashboard")

# Tabs for each data type
tab1, tab2, tab3 = st.tabs(["🌦️ Weather", "🗞️ News", "📬 Posts"])

# Weather Tab
with tab1:
    st.header("🌦️ Weather Data")
    if not weather_df.empty:
        cities = weather_df['name'].dropna().unique()
        selected_city = st.selectbox("City", sorted(cities))
        city_data = weather_df[weather_df["name"] == selected_city]
        date_range = st.date_input("Filter by Date Range", [])
        if len(date_range) == 2:
            start_date, end_date = pd.to_datetime(date_range)
            city_data = city_data[(city_data["fetched_at"] >= start_date) & (city_data["fetched_at"] <= end_date)]

        if not city_data.empty:
            st.subheader("Temperature Trend (°C)")
            fig = px.line(city_data, x="fetched_at", y=["main.temp"], title="Temperature Over Time")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(city_data[["fetched_at", "weather", "main"]])
        else:
            st.warning("No data found for selected filters.")
    else:
        st.error("Weather data not available.")

# News Tab
with tab2:
    st.header("🗞️ News Articles")
    if not news_df.empty:
        keyword = st.text_input("Keyword in Title or Description", "")
        date_range = st.date_input("Fetch Date Range", [])
        filtered_news = news_df.copy()
        if keyword:
            filtered_news = filtered_news[
                filtered_news['title'].str.contains(keyword, case=False, na=False) |
                filtered_news['description'].str.contains(keyword, case=False, na=False)
            ]
        if len(date_range) == 2:
            start_date, end_date = pd.to_datetime(date_range)
            filtered_news = filtered_news[
                (filtered_news["fetched_at"] >= start_date) & 
                (filtered_news["fetched_at"] <= end_date)
            ]
        if not filtered_news.empty:
            st.subheader("News Source Frequency")
            count_df = filtered_news['source'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).value_counts().reset_index()
            count_df.columns = ['Source', 'Articles']
            fig = px.bar(count_df, x='Source', y='Articles', title='Number of Articles per Source')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(filtered_news[["title", "description", "fetched_at"]])
        else:
            st.warning("No news articles match your filters.")
    else:
        st.error("News data not available.")

# Posts Tab
with tab3:
    st.header("📬 User Posts")
    if not posts_df.empty:
        user_ids = posts_df["userId"].dropna().unique()
        selected_user = st.selectbox("Filter by User ID", sorted(user_ids))
        keyword = st.text_input("Search Keyword in Title/Body", "")
        date_range = st.date_input("Fetch Date Range", [])

        filtered_posts = posts_df[posts_df["userId"] == selected_user]
        if keyword:
            filtered_posts = filtered_posts[
                filtered_posts["title"].str.contains(keyword, case=False, na=False) |
                filtered_posts["body"].str.contains(keyword, case=False, na=False)
            ]
        if len(date_range) == 2:
            start_date, end_date = pd.to_datetime(date_range)
            filtered_posts = filtered_posts[
                (filtered_posts["fetched_at"] >= start_date) &
                (filtered_posts["fetched_at"] <= end_date)
            ]
        if not filtered_posts.empty:
            st.subheader("Posts Over Time")
            post_counts = filtered_posts.groupby(filtered_posts["fetched_at"].dt.date).size().reset_index(name='Post Count')
            fig = px.line(post_counts, x='fetched_at', y='Post Count', title="Posts Per Day")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("User-wise Post Count")
            user_counts = posts_df.groupby("userId").size().reset_index(name="Count")
            fig2 = px.bar(user_counts, x="userId", y="Count", title="Total Posts Per User")
            st.plotly_chart(fig2, use_container_width=True)

            st.dataframe(filtered_posts[["userId", "title", "body", "fetched_at"]])
        else:
            st.warning("No posts match your filters.")
    else:
        st.error("Posts data not available.")

        st.error("Posts data not available.")
