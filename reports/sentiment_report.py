import pandas as pd


def generate_sentiment_report(results):
    if not results:
        raise ValueError("No results available for report")

    df = pd.DataFrame(results)

    summary = {
        "total_samples": len(df),
        "positive": (df["sentiment"] == "Positive").sum(),
        "negative": (df["sentiment"] == "Negative").sum(),
        "neutral": (df["sentiment"] == "Neutral").sum()
    }

    return df, summary