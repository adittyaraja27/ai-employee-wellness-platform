from recommendation.hybrid import generate_hybrid_recommendations


emotion_result = {
    "primary_emotion": "fear"
}

intensity_result = {
    "severity": "High"
}


recommendations = generate_hybrid_recommendations(
    emotion_result,
    intensity_result
)


print("\nHybrid Recommendations\n")

for item in recommendations:

    print(
        f"{item['content']['title']} "
        f"→ Score: {item['score']}"
    )