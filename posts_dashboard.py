import streamlit as st
import pandas as pd
import json
import os

def posts_dashboard(user_id_filter=None, search_term=None, date_range=None):
    file_path = "data_lake/posts_data.json"
    if not os.path.exists(file_path):
        st.error("No posts data found. Please run fetch_posts.py first.")
        return

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
            df = pd.DataFrame(data)
        except json.JSONDecodeError:
            st.error("Invalid JSON format in posts_data.json.")
            return

    df['fetched_at'] = pd.to_datetime(df['fetched_at'], errors='coerce')
    df.dropna(subset=['fetched_at'], inplace=True)

    if user_id_filter is not None:
        df = df[df['userId'] == user_id_filter]

    if date_range is not None:
        start_date, end_date = date_range
        df = df[(df['fetched_at'].dt.date >= start_date) & (df['fetched_at'].dt.date <= end_date)]

    if search_term:
        df = df[
            df['title'].str.contains(search_term, case=False, na=False) |
            df['body'].str.contains(search_term, case=False, na=False)
        ]

    if df.empty:
        st.warning("No posts data found for given filters.")
        return

    st.subheader("📬 Posts Data")
    st.write(df[['userId', 'title', 'body', 'fetched_at']])

    # Visualizations
    user_counts = df['userId'].value_counts().sort_index()
    st.write("### Posts per User ID")
    st.bar_chart(user_counts)

    posts_over_time = df.groupby(df['fetched_at'].dt.date).size()
    st.write("### Posts over Time")
    st.line_chart(posts_over_time)

