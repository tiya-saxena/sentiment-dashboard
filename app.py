import streamlit as st
import pandas as pd
import plotly.express as px

COLORS = {"Positive": "#00FF7F",
          "Negative": "#FF69B4",
          "Neutral":  "#008B8B"}

st.title("💬 Sentiment Dashboard")

# Load file
try:
    df = pd.read_csv("cleaned_1000.csv")
except:
    st.error("❌ Could not load file!")
    st.stop()

# Fix date
df["date"]  = pd.to_datetime(df["date"], errors="coerce")
df          = df.dropna(subset=["date"])
df["hour"]  = df["date"].dt.hour
df["month"] = df["date"].dt.month_name()
df["day"]   = df["date"].dt.day_name()

# ── Tabs ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 Data", "🥧 Breakdown", "📈 Over Time"])

# ── Tab 1 ────────────────────────────────────────────
with tab1:
    st.subheader("📋 Cleaned Data")
    num_rows = st.slider("How many rows to show?",
                          min_value=10, max_value=len(df),
                          value=20, step=10)
    st.dataframe(df[["text", "clean_text", "sentiment"]].head(num_rows))

# ── Tab 2 ────────────────────────────────────────────
with tab2:
    st.subheader("🥧 Sentiment Breakdown")
    fig = px.pie(df, names="sentiment",
                 title="Sentiment Breakdown",
                 color="sentiment",
                 color_discrete_map=COLORS)
    st.plotly_chart(fig)

    st.subheader("📊 Sentiment Count")
    fig2 = px.histogram(df, x="sentiment",
                        color="sentiment",
                        color_discrete_map=COLORS)
    st.plotly_chart(fig2)

# ── Tab 3 ────────────────────────────────────────────
with tab3:

    st.subheader("🕐 Sentiment by Hour")
    hourly = df.groupby(["hour","sentiment"]).size().reset_index(name="count")
    fig3 = px.line(hourly, x="hour", y="count",
                   color="sentiment",
                   title="Sentiment by Hour",
                   color_discrete_map=COLORS,
                   markers=True)
    st.plotly_chart(fig3)

    st.subheader("📅 Sentiment by Day")
    day_order = ["Monday","Tuesday","Wednesday",
                 "Thursday","Friday","Saturday","Sunday"]
    daily = df.groupby(["day","sentiment"]).size().reset_index(name="count")
    daily["day"] = pd.Categorical(daily["day"],
                                   categories=day_order,
                                   ordered=True)
    daily = daily.sort_values("day")
    fig4 = px.bar(daily, x="day", y="count",
                  color="sentiment",
                  title="Sentiment by Day",
                  color_discrete_map=COLORS)
    st.plotly_chart(fig4)

    st.subheader("📆 Sentiment by Month")
    month_order = ["January","February","March","April",
                   "May","June","July","August",
                   "September","October","November","December"]
    monthly = df.groupby(["month","sentiment"]).size().reset_index(name="count")
    monthly["month"] = pd.Categorical(monthly["month"],
                                       categories=month_order,
                                       ordered=True)
    monthly = monthly.sort_values("month")
    fig5 = px.bar(monthly, x="month", y="count",
                  color="sentiment",
                  title="Sentiment by Month",
                  color_discrete_map=COLORS)
    st.plotly_chart(fig5)