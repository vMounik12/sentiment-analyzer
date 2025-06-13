import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("local_s3_bucket/sentiment_data.csv")

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Title
st.title("📊 Sentiment Analysis Dashboard")

# Show raw data
if st.checkbox("Show raw data"):
    st.write(df)

# Sentiment count
st.subheader("🔹 Sentiment Distribution")
sentiment_counts = df['sentiment'].value_counts()
st.bar_chart(sentiment_counts)

# Monthly sentiment trend
st.subheader("🔹 Average Sentiment Score by Month")
monthly_avg = df.groupby("month")["score"].mean()
st.line_chart(monthly_avg)

# Pie chart
st.subheader("🔹 Sentiment Percentage")
st.write(sentiment_counts)
st.pyplot(plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')[0].figure)
