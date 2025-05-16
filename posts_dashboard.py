import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

# Title
st.title("📬 Posts Data Dashboard")

# File path
file_path = "data_lake/posts_data.json"

# Check if file exists
if not os.path.exists(file_path):
    st.error("No posts data found. Please run fetch_posts.py first.")
    st.stop()

# Load data
with open(file_path, "r") as f:
    try:
        data = json.load(f)
        df = pd.DataFrame(data)
    except json.JSONDecodeError:
        st.error("Invalid JSON format in posts_data.json.")
        st.stop()

# Convert date
df['fetched_at'] = pd.to_datetime(df['fetched_at'], errors='coerce')
df.dropna(subset=['fetched_at'], inplace=True)

# Sidebar filters
st.sidebar.header("🔍 Filters")

# User ID filter
user_ids = sorted(df['userId'].dropna().unique())
selected_users = st.sidebar.multiselect("Select User ID(s)", user_ids, default=user_ids)

# Keyword search
search_term = st.sidebar.text_input("Search Keyword in Title or Body")

# Date range
min_date = df['fetched_at'].min()
max_date = df['fetched_at'].max()
start_date, end_date = st.sidebar.date_input("Date Range", [min_date.date(), max_date.date()])

# Apply filters
filtered_df = df[df['userId'].isin(selected_users)]
filtered_df = filtered_df[
    (filtered_df['fetched_at'].dt.date >= start_date) & 
    (filtered_df['fetched_at'].dt.date <= end_date)
]

if search_term:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_term, case=False, na=False) |
        filtered_df['body'].str.contains(search_term, case=False, na=False)
    ]

# Show filtered data
st.subheader("📄 Filtered Posts")
st.write(filtered_df[['userId', 'title', 'body', 'fetched_at']])

# Visualization section
st.subheader("📊 Visualizations")

# 1. Posts per user
if not filtered_df.empty:
    user_counts = filtered_df['userId'].value_counts().sort_index()
    st.write("### Posts per User ID")
    st.bar_chart(user_counts)

    # 2. Posts over time
    posts_over_time = filtered_df.groupby(filtered_df['fetched_at'].dt.date).size()
    st.write("### Posts over Time")
    st.line_chart(posts_over_time)
else:
    st.warning("No data available for selected filters.")

