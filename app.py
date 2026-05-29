import streamlit as st
import pandas as pd
import plotly.express as px

COLORS = {"Positive": "#00FF7F",
          "Negative": "#FF69B4",
          "Neutral":  "#008B8B"}

st.title("💬 Sentiment Dashboard")

# Load file
df = pd.read_csv("cleaned_1000.csv")

# Fix date safely
df["date"] = pd.to_datetime(df["date"], errors="coerce")
# Drop rows where date failed to parse
df = df.dropna(subset=["date"])

# Extract time parts
df["hour"]  = df["date"].dt.hour
df["month"] = df["date"].dt.month_name()
df["day"]   = df["date"].dt.day_name()

# ── Tabs ────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 Data", "🥧 Breakdown", "📈 Over Time"])

# ── Tab 1 ───────────────────────────────────────────
with tab1:
    st.subheader("📋 Cleaned Data")
    num_rows = st.slider("How many rows to show?",
                          min_value=10, max_value=1000,
                          value=20, step=10)
    st.dataframe(df[["text", "clean_text", "sentiment"]].head(num_rows))

# ── Tab 2 ───────────────────────────────────────────
with tab2:
    st.subheader("🥧 Sentiment Breakdown")
    fig = px.pie(df, names="sentiment", title="Sentiment Breakdown",
                 color="sentiment", color_discrete_map=COLORS)
    st.plotly_chart(fig)

    st.subheader("📊 Sentiment Count")
    fig2 = px.histogram(df, x="sentiment", color="sentiment",
                        color_discrete_map=COLORS)
    st.plotly_chart(fig2)

# ── Tab 3 ───────────────────────────────────────────
with tab3:

    # Debug — show date sample
    st.write("📅 Sample dates:", df["date"].head(3).tolist())
    st.write("Total rows with valid date:", len(df))

    # Hourly
    st.subheader("🕐 Sentiment by Hour")
    hourly = df.groupby(["hour", "sentiment"]).size().reset_index(name="count")
    if hourly.empty:
        st.warning("⚠️ No hourly data found!")
    else:
        fig3 = px.line(hourly, x="hour", y="count", color="sentiment",
                       title="Sentiment by Hour",
                       color_discrete_map=COLORS, markers=True)
        st.plotly_chart(fig3)

    # Daily
    st.subheader("📅 Sentiment by Day")
    day_order = ["Monday","Tuesday","Wednesday",
                 "Thursday","Friday","Saturday","Sunday"]
    daily = df.groupby(["day", "sentiment"]).size().reset_index(name="count")
    daily["day"] = pd.Categorical(daily["day"],
                                   categories=day_order, ordered=True)
    daily = daily.sort_values("day")
    if daily.empty:
        st.warning("⚠️ No daily data found!")
    else:
        fig4 = px.bar(daily, x="day", y="count", color="sentiment",
                      title="Sentiment by Day",
                      color_discrete_map=COLORS)
        st.plotly_chart(fig4)

    # Monthly
    st.subheader("📆 Sentiment by Month")
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    monthly = df.groupby(["month","sentiment"]).size().reset_index(name="count")
    monthly["month"] = pd.Categorical(monthly["month"],
                                       categories=month_order, ordered=True)
    monthly = monthly.sort_values("month")
    if monthly.empty:
        st.warning("⚠️ No monthly data found!")
    else:
        fig5 = px.bar(monthly, x="month", y="count", color="sentiment",
                      title="Sentiment by Month",
                      color_discrete_map=COLORS)
        st.plotly_chart(fig5)
        # updated