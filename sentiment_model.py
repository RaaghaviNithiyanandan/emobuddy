import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER model (only required once, might need try/except in some environments)
try:
    nltk.data.find("vader_lexicon")
except LookupError:
    nltk.download("vader_lexicon")


# Load Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Returns sentiment label (positive, neutral, negative)"""
    scores = sia.polarity_scores(text)
    if scores["compound"] >= 0.05:
        return "positive"
    elif scores["compound"] <= -0.05:
        return "negative"
    else:
        return "neutral"
