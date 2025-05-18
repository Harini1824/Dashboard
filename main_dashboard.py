import streamlit as st
from weather_dashboard import weather_dashboard
from news_dashboard import news_dashboard
from posts_dashboard import posts_dashboard
import datetime

def main_dashboard():
    st.title("Data Dashboard")

    st.sidebar.header("Common Filters")

    # Common input example (like Patient ID or Name)
    user_id_input = st.sidebar.text_input("Enter User ID (for Posts)")
    city_input = st.sidebar.text_input("Enter City (for Weather)")
    news_keyword_input = st.sidebar.text_input("Enter Keyword (for News)")

    # Date range filter for posts (optional)
    date_range = st.sidebar.date_input("Posts Date Range", [datetime.date(2000,1,1), datetime.date.today()])

    # Call dashboards with filtered data
    st.markdown("---")
    weather_dashboard(city_filter=city_input)

    st.markdown("---")
    news_dashboard(keyword_filter=news_keyword_input)

    st.markdown("---")
    user_id = None
    if user_id_input:
        try:
            user_id = int(user_id_input)
        except ValueError:
            st.sidebar.error("User ID must be an integer.")
    posts_dashboard(user_id_filter=user_id, date_range=date_range)

if __name__ == "__main__":
    main_dashboard()
