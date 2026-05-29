import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print("🚀 Program Started...")

# Load file
df = pd.read_excel("dataset.xlsx", header=None, nrows=1000)
df.columns = ["target", "id", "date", "flag", "user", "text"]
print("✅ File Loaded! Rows:", len(df))

# Remove nulls & duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Create clean_text column
df["clean_text"] = df["text"].apply(lambda x: re.sub(r"http\S+", "", str(x)))
df["clean_text"] = df["clean_text"].apply(lambda x: re.sub(r"[@#]\S+", "", x))
df["clean_text"] = df["clean_text"].str.lower().str.strip()
print("✅ Text Cleaned!")

# Run VADER
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:    return "Positive"
    elif score <= -0.05: return "Negative"
    else:                return "Neutral"

df["sentiment"] = df["clean_text"].apply(get_sentiment)
print("✅ Sentiment Done!")

# Save
df.to_csv("cleaned_1000.csv", index=False)
print("✅ Saved as cleaned_1000.csv")