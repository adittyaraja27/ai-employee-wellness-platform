from preprocessing.text_preprocessor import preprocess_text
from sentiment.vader_analyzer import analyze_sentiment
from reports.sentiment_report import generate_sentiment_report


texts = [
    "I absolutely love my job!",
    "I am feeling exhausted and stressed because of my workload.",
    "The meeting is scheduled for 3 PM.",
    "I am very happy with my team.",
    "I am frustrated with my workload."
]


results = []


for text in texts:

    processed_text = preprocess_text(text)

    sentiment_result = analyze_sentiment(text)

    result = {
        "input_text": text,
        "processed_text": processed_text,
        "sentiment": sentiment_result["sentiment"],
        "positive": sentiment_result["positive"],
        "negative": sentiment_result["negative"],
        "neutral": sentiment_result["neutral"],
        "compound": sentiment_result["compound"]
    }

    results.append(result)


# Generate report
report, summary = generate_sentiment_report(results)

print("\nSENTIMENT REPORT\n")
print(report.to_string(index=False))

print("\nSUMMARY")
print("Total samples:", summary["total_samples"])
print("Positive:", summary["positive"])
print("Negative:", summary["negative"])
print("Neutral:", summary["neutral"])