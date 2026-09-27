from recommendation.hybrid import HybridRecommendationEngine


engine = HybridRecommendationEngine()


emotion_result = {
    "primary_emotion": "fear"
}


intensity_result = {
    "severity": "High"
}


user_preferences = {
    "activities": ["walking"],
    "content_types": [],
    "interests": []
}


text = "I'm extremely anxious about my upcoming presentation."


recommendations = engine.generate_recommendations(
    user_text=text,
    emotion_result=emotion_result,
    intensity_result=intensity_result,
    user_preferences=user_preferences
)


print("\nHybrid Recommendation Results\n")


for item in recommendations:

    breakdown = item["score_breakdown"]

    print(
        f"\n{item['content']['title']}"
    )

    print(
        f"  Emotion: {breakdown['emotion_score']}"
    )

    print(
        f"  Intensity: {breakdown['intensity_score']}"
    )

    print(
        f"  Preference: {breakdown['preference_score']}"
    )

    print(
        f"  Semantic: {breakdown['semantic_score']:.4f}"
    )

    print(
        f"  Final Score: {breakdown['final_score']:.4f}"
    )