from sentiment.vader_analyzer import analyze_sentiment


texts = [
    "I absolutely love my job!",
    "I hate my job. It is terrible.",
    "The meeting is scheduled for 3 PM.",
    "I am feeling exhausted and stressed because of my workload.",
    "I am very happy with my team.",
    "Work has been okay lately.",
    "I am frustrated, but I still enjoy working here.",
    "I don't feel good about my current workload."
]


for text in texts:
    result = analyze_sentiment(text)

    print("\nText:", text)
    print("Sentiment:", result["sentiment"])
    print("Positive:", result["positive"])
    print("Negative:", result["negative"])
    print("Neutral:", result["neutral"])
    print("Compound:", result["compound"])


print("\nInvalid input tests:")

invalid_inputs = [
    "",
    "     ",
    None
]

for text in invalid_inputs:
    try:
        result = analyze_sentiment(text)
        print("Unexpectedly accepted:", repr(text))

    except ValueError as e:
        print("Correctly rejected:", repr(text))