import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px

file_path = "data_lake/news_data.json"

@st.cache_data
def load_news_data(path):
    with open(path, "r") as f:
        data = json.load(f)
    records = []
    for article in data:
        records.append({
            "source": article.get("source", {}).get("name", ""),
            "author": article.get("author"),
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt"),
            "fetched_at": article.get("fetched_at"),
        })
    df = pd.DataFrame(records)

    # Convert dates to datetime
    df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")
    df["fetched_at"] = pd.to_datetime(df["fetched_at"], errors="coerce")

    return df

st.title("🗞️ News Data Dashboard")

# Load and check data
try:
    df = load_news_data(file_path)
except FileNotFoundError:
    st.error("No news data file found. Please run fetch_news.py first.")
    st.stop()

if df.empty:
    st.warning("News data is empty.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Source filter
sources = df["source"].dropna().unique()
selected_source = st.sidebar.multiselect("Select Source(s)", options=sources, default=list(sources))

# Safe min/max date setup
if df["publishedAt"].notna().any():
    min_date = df["publishedAt"].min().date()
    max_date = df["publishedAt"].max().date()
else:
    st.error("No valid 'publishedAt' timestamps found in your data.")
    st.stop()

start_date = st.sidebar.date_input("Start Published Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Published Date", max_date, min_value=min_date, max_value=max_date)

# Keyword filter
keyword = st.sidebar.text_input("Search Keyword in Title (optional)")

# Apply filters
filtered_df = df[
    (df["source"].isin(selected_source)) &
    (df["publishedAt"].dt.date >= start_date) &
    (df["publishedAt"].dt.date <= end_date)
]

if keyword:
    filtered_df = filtered_df[filtered_df["title"].str.contains(keyword, case=False, na=False)]

# Display filtered data
st.subheader(f"📄 Filtered Articles ({len(filtered_df)})")
if not filtered_df.empty:
    st.dataframe(filtered_df[["publishedAt", "source", "title", "url"]])
else:
    st.warning("No articles found for the selected filters.")
    st.stop()

# Chart selection
st.subheader("📊 Visualize News Trends")
chart_option = st.selectbox("Choose a graph to display:", ["Articles Over Time", "Articles by Source"])

fig = None
if chart_option == "Articles Over Time":
    trend = filtered_df.groupby(filtered_df["publishedAt"].dt.date).size().reset_index(name="Count")
    fig = px.line(trend, x="publishedAt", y="Count", title="Articles Over Time", markers=True)
elif chart_option == "Articles by Source":
    source_count = filtered_df["source"].value_counts().reset_index()
    source_count.columns = ["Source", "Count"]
    fig = px.bar(source_count, x="Source", y="Count", title="Articles by Source")

st.plotly_chart(fig, use_container_width=True)

