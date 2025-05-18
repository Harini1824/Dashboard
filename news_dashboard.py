import streamlit as st
import pandas as pd
import json
import os

def news_dashboard(keyword_filter=None):
    file_path = "data_lake/news_data.json"
    if not os.path.exists(file_path):
        st.error("No news data found. Please run fetch_news.py first.")
        return

    with open(file_path, "r") as f:
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
    df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")

    if keyword_filter:
        df = df[
            df["title"].str.contains(keyword_filter, case=False, na=False) |
            df["description"].str.contains(keyword_filter, case=False, na=False)
        ]

    if df.empty:
        st.warning("No news data found for this keyword.")
        return

    st.subheader("🗞️ News Data")
    st.write(df[["publishedAt", "source", "title"]])

    # Visualization: articles over time
    posts_over_time = df.groupby(df["publishedAt"].dt.date).size()
    st.line_chart(posts_over_time)


