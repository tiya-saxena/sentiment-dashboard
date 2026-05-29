import streamlit as st
import pandas as pd
import plotly.express as px

COLORS = {"Positive": "#00FF7F",   # Bright Lime Green
          "Negative": "#FF69B4",   # Hot Pink
          "Neutral":  "#008B8B"}   # Dark Teal

st.title("💬 Sentiment Dashboard")

df = pd.read_csv("cleaned_1000.csv")

df["date"]  = pd.to_datetime(df["date"], errors="coerce")
df["hour"]  = df["date"].dt.hour
df["month"] = df["date"].dt.month_name()
df["day"]   = df["date"].dt.day_name()

tab1, tab2, tab3 = st.tabs(["📋 Data", "🥧 Breakdown", "📈 Over Time"])

with tab1:
    st.subheader("📋 Cleaned Data")
    st.dataframe(df[["text", "clean_text", "sentiment"]].head(20))

with tab2:
    st.subheader("🥧 Sentiment Breakdown")
    fig = px.pie(df, names="sentiment", title="Sentiment Breakdown",
                 color="sentiment", color_discrete_map=COLORS)
    st.plotly_chart(fig)

    st.subheader("📊 Sentiment Count")
    fig2 = px.histogram(df, x="sentiment", color="sentiment",
                        color_discrete_map=COLORS)
    st.plotly_chart(fig2)

with tab3:

    st.subheader("🕐 Sentiment by Hour of Day")
    hourly = df.groupby(["hour", "sentiment"]).size().reset_index(name="count")
    fig3 = px.line(hourly, x="hour", y="count", color="sentiment",
                   title="Sentiment Trend by Hour",
                   color_discrete_map=COLORS, markers=True)
    fig3.update_layout(xaxis_title="Hour (0-23)", yaxis_title="Number of Tweets")
    st.plotly_chart(fig3)

    st.subheader("📅 Sentiment by Day of Week")
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    daily = df.groupby(["day", "sentiment"]).size().reset_index(name="count")
    daily["day"] = pd.Categorical(daily["day"], categories=day_order, ordered=True)
    daily = daily.sort_values("day")
    fig4 = px.bar(daily, x="day", y="count", color="sentiment",
                  title="Sentiment by Day of Week",
                  color_discrete_map=COLORS)
    fig4.update_layout(xaxis_title="Day", yaxis_title="Number of Tweets")
    st.plotly_chart(fig4)

    st.subheader("📆 Sentiment by Month")
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    monthly = df.groupby(["month", "sentiment"]).size().reset_index(name="count")
    monthly["month"] = pd.Categorical(monthly["month"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("month")
    fig5 = px.bar(monthly, x="month", y="count", color="sentiment",
                  title="Sentiment by Month",
                  color_discrete_map=COLORS)
    fig5.update_layout(xaxis_title="Month", yaxis_title="Number of Tweets")
    st.plotly_chart(fig5)