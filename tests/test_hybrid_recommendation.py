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


# ---------------------------------------
# 1. Generate recommendations BEFORE feedback
# ---------------------------------------

recommendations_before = engine.generate_recommendations(
    user_text=text,
    emotion_result=emotion_result,
    intensity_result=intensity_result,
    user_preferences=user_preferences
)


print("\nHybrid Recommendation Results - Before Feedback\n")


for item in recommendations_before:

    breakdown = item["score_breakdown"]

    print(f"\n{item['content']['title']}")

    print(f"  Emotion: {breakdown['emotion_score']}")
    print(f"  Intensity: {breakdown['intensity_score']}")
    print(f"  Preference: {breakdown['preference_score']}")
    print(f"  Semantic: {breakdown['semantic_score']:.4f}")
    print(f"  Feedback: {breakdown['feedback_score']:.4f}")
    print(f"  Final Score: {breakdown['final_score']:.4f}")


# ---------------------------------------
# 2. Give positive feedback to walking
# ---------------------------------------

engine.feedback.record_feedback(
    recommendation_id="walk_01",
    viewed=True,
    accepted=True,
    rating=5
)

engine.feedback.record_feedback(
    recommendation_id="walk_01",
    viewed=True,
    accepted=True,
    rating=5
)


# ---------------------------------------
# 3. Generate recommendations AFTER feedback
# ---------------------------------------

recommendations_after = engine.generate_recommendations(
    user_text=text,
    emotion_result=emotion_result,
    intensity_result=intensity_result,
    user_preferences=user_preferences
)


print("\n\nHybrid Recommendation Results - After Feedback\n")


for item in recommendations_after:

    breakdown = item["score_breakdown"]

    print(f"\n{item['content']['title']}")

    print(f"  Emotion: {breakdown['emotion_score']}")
    print(f"  Intensity: {breakdown['intensity_score']}")
    print(f"  Preference: {breakdown['preference_score']}")
    print(f"  Semantic: {breakdown['semantic_score']:.4f}")
    print(f"  Feedback: {breakdown['feedback_score']:.4f}")
    print(f"  Final Score: {breakdown['final_score']:.4f}")


# ---------------------------------------
# 4. Find walk_01 before and after
# ---------------------------------------

walk_before = next(
    item
    for item in recommendations_before
    if item["content"]["id"] == "walk_01"
)

walk_after = next(
    item
    for item in recommendations_after
    if item["content"]["id"] == "walk_01"
)


# ---------------------------------------
# 5. Verify feedback improved the score
# ---------------------------------------

assert walk_before["score_breakdown"]["feedback_score"] == 0

assert walk_after["score_breakdown"]["feedback_score"] > 0

assert walk_after["score"] > walk_before["score"]


print("\nFEEDBACK LEARNING TEST PASSED")