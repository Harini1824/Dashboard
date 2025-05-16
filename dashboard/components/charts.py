import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter

# Weather Chart
def create_weather_chart(data, chart_type="Line"):
    df = pd.DataFrame([{
        "Date": datetime.fromisoformat(item["fetched_at"]).strftime("%Y-%m-%d"),
        "Temperature": item["main"]["temp"]
    } for item in data])

    st.write(df)

    if chart_type == "Line":
        st.line_chart(df.set_index("Date")["Temperature"])
    elif chart_type == "Bar":
        st.bar_chart(df.set_index("Date")["Temperature"])
    elif chart_type == "Pie":
        fig, ax = plt.subplots()
        ax.pie(df["Temperature"], labels=df["Date"], autopct='%1.1f%%')
        st.pyplot(fig)

# Posts Chart
def create_post_chart(data, chart_type="Bar"):
    df = pd.DataFrame(data)
    user_counts = df["userId"].value_counts()

    if chart_type == "Bar":
        st.bar_chart(user_counts)
    elif chart_type == "Pie":
        fig, ax = plt.subplots()
        ax.pie(user_counts, labels=user_counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

# News Chart
def create_news_chart(data, chart_type="Bar"):
    sources = [item["source"]["name"] for item in data]
    count = Counter(sources)
    df = pd.DataFrame(count.items(), columns=["Source", "Count"])

    if chart_type == "Bar":
        st.bar_chart(df.set_index("Source"))
    elif chart_type == "Pie":
        fig, ax = plt.subplots()
        ax.pie(df["Count"], labels=df["Source"], autopct='%1.1f%%')
        st.pyplot(fig)
